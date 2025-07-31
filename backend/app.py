from flask import Flask,request,jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello():
    return "HELLO"

@app.route("/scrape")
def scrape_website():
    url = request.args.get('url')
    if not url:
        return jsonify({"error":"URL NOT FOUND"}),400
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content,'html.parser')
        text = soup.get_text(separator=' ',strip=True)
        return jsonify({"scraped_text":text})
    except requests.exceptions.RequestException as e:
        return jsonify({"error":"Failed to fetch"}),500