import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai


app = Flask(__name__)
CORS(app)


try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not found in environment")

    genai.configure(api_key=api_key)

    # list available models so you can pick a supported one
    models = genai.list_models()
    print("Available models:", [getattr(m, "name", str(m)) for m in models])

    # pick a preferred model if present, otherwise fallback to the first listed model
    preferred = next((getattr(m, "name", m) for m in models if "gemini" in getattr(m, "name", "").lower() or "bison" in getattr(m, "name", "").lower()), None)
    chosen_model_name = preferred or (getattr(models[0], "name", str(models[0])) if models else None)
    if not chosen_model_name:
        raise RuntimeError("No models returned by list_models()")

    # Try to create a GenerativeModel wrapper; if that fails, keep model as a string and use top-level generate call later
    try:
        model = genai.GenerativeModel(chosen_model_name)
        print("Using GenerativeModel wrapper:", chosen_model_name)
    except Exception:
        model = chosen_model_name
        print("Will use top-level generate call with model name:", chosen_model_name)

except Exception as e:
    print(f"ERROR: {e}")
    model = None




# --- AI Helper Function ---
def generate_checklist(scraped_text: str) -> str:
    """
    Generates a checklist by calling the available generative model API.
    """
    if not model:
        msg = "Model not available"
        print(msg)
        return msg

    prompt_parts = [
        "You are an expert at creating clear, concise, and actionable user onboarding guides from documentation.",
        "First, silently identify the key phases of a new user's journey based on the provided text (e.g., Account Setup, First Project, Inviting Teammates, Advanced Features).",
        "Then, using those phases as a guide, generate a step-by-step onboarding checklist. Each step should be a clear, actionable item. Define these steps in detail.",
        "Do not include a title or the word 'Checklist' in your response. Do not use markdown formatting like asterisks or checkboxes. Begin directly with the first step.",
        f"TEXT: \"{scraped_text[:4000]}\"",
    ]
    prompt_text = "\n".join(prompt_parts)

    try:
        # Prefer model wrapper if it provides a generate method
        if hasattr(model, "generate_content"):
            resp = model.generate_content(prompt_text)
            return getattr(resp, "text", str(resp))

        if hasattr(model, "generate"):
            resp = model.generate(prompt_text)
            return getattr(resp, "text", str(resp))

        # If model is a string, try top-level genai functions (try common names)
        if isinstance(model, str):
            for fn_name in ("generate_text", "generate", "generate_content"):
                fn = getattr(genai, fn_name, None)
                if not fn:
                    continue
                try:
                    # many genai APIs accept either `model`+`input` or `model`+`prompt`
                    try:
                        resp = fn(model=model, input=prompt_text)
                    except TypeError:
                        resp = fn(model=model, prompt=prompt_text)
                    return getattr(resp, "text", str(resp))
                except Exception:
                    continue

        return "Unsupported model object or client API"

    except Exception as e:
        error_msg = f"Error generating checklist: {e}"
        print(error_msg)
        return error_msg


@app.route("/")
def hello():
    return "This is the AI Checklist Generator Backend"

@app.route("/scrape")
def scrape_website():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        checklist_text = generate_checklist(text)
        checklist_items = [item.strip().lstrip('* []-') for item in checklist_text.split('\n') if item.strip()]
        return jsonify({"onboarding_checklist": checklist_items})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch URL: {e}"}), 500