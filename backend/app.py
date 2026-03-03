import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai  # Ensure you have 'google-genai' installed

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Initialize Gemini Client ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not found in environment")

    # The modern SDK uses genai.Client
    client = genai.Client(api_key=api_key)
    MODEL_ID = "gemini-2.0-flash" # Recommended latest model
except Exception as e:
    print(f"INITIALIZATION ERROR: {e}")
    client = None

def generate_checklist(scraped_text: str) -> str:
    """
    Generates a checklist using the official SDK methods.
    """
    if not client:
        return "Model client not initialized."

    prompt = (
        "You are an expert at creating clear, concise, and actionable user onboarding guides. "
        "Based on the text below, generate a step-by-step onboarding checklist. "
        "Each step should be a clear, actionable item. "
        "Do not include a title, checkboxes, or markdown asterisks. "
        f"\n\nTEXT: {scraped_text[:5000]}"
    )

    try:
        # Standard call for the google-genai SDK
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating checklist: {str(e)}"

@app.route("/scrape")
def scrape_website():
    url = request.args.get('url')
    print("This is the url")
    print(url)
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    try:
        # Set a timeout and user-agent to avoid getting blocked
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Strip script and style elements to get cleaner text
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        
        checklist_text = generate_checklist(text)
        
        # Clean up the response into a list
        checklist_items = [
            item.strip().lstrip('1234567890. ') 
            for item in checklist_text.split('\n') 
            if item.strip()
        ]
        
        return jsonify({"onboarding_checklist": checklist_items})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)