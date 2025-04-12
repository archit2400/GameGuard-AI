from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

PERSPECTIVE_API_KEY = "AIzaSyAr-KB5ebUUcokY9Z5jZ0qmnKUPbzcz7_Q"
PERSPECTIVE_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"

def analyze_message(text):
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "SPAM": {}
        }
    }
    response = requests.post(PERSPECTIVE_URL, data=json.dumps(data))
    result = response.json()

    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    flagged = toxicity_score > 0.7
    block_warning = toxicity_score > 0.85

    return flagged, block_warning, toxicity_score

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    text = data["message"]
    flagged, block_warning, toxicity = analyze_message(text)
    return jsonify({
        "flagged": flagged,
        "block_warning": block_warning,
        "toxicity": toxicity
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
