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
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model loaded succedfully")
except Exception as e:
    print("ERROR"+e)
    model=None



# --- AI Helper Function ---
def generate_checklist(scraped_text: str) -> str:
    """
    Generates a checklist by calling the Hugging Face OpenAI-compatible API.
    """
    if not model:
        print("Model not available")
    try:

        # 3. Create the prompt for the AI
        prompt = [
            "You are an expert at creating clear, concise, and actionable user onboarding guides from documentation.",
            "First, silently identify the key phases of a new user's journey based on the provided text (e.g., Account Setup, First Project, Inviting Teammates, Advanced Features).",
            "Then, using those phases as a guide, generate a step-by-step onboarding checklist. Each step should be a clear, actionable item.Define these steps in detai;",
            "Do not include a title or the word 'Checklist' in your response. Do not use markdown formatting like asterisks or checkboxes. Begin directly with the first step.",
            f"TEXT: \"{scraped_text[:4000]}\"",
        ]
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_msg = f"Error generating checklist: {e}"
        print(error_msg)
        return error_msg

# --- Flask API Routes ---
@app.route("/")
def hello():
    return "This is the AI Checklist Generator Backend"

@app.route("/scrape")
def scrape_website():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    try:
        # Scrape website content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # Get the AI-generated checklist
        checklist_text = generate_checklist(text)
        checklist_items = [item.strip().lstrip('* []-') for item in checklist_text.split('\n') if item.strip()]
        return jsonify({"onboarding_checklist": checklist_items})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch URL: {e}"}), 500