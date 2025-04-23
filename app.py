from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import time

app = Flask(__name__)

PERSPECTIVE_API_KEY = "AIzaSyAr-KB5ebUUcokY9Z5jZ0qmnKUPbzcz7_Q"
PERSPECTIVE_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"

# In-memory store for user toxicity tracking
user_violations = {}
user_blocked_until = {}

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
    user_id = data.get("user_id", "default_user")  # fallback user ID

    # Check if user is currently blocked
    current_time = time.time()
    if user_id in user_blocked_until and current_time < user_blocked_until[user_id]:
        seconds_remaining = int(user_blocked_until[user_id] - current_time)
        return jsonify({
            "blocked": True,
            "message": f"You are blocked for {seconds_remaining} more seconds."
        })

    flagged, block_warning, toxicity = analyze_message(text)

    # Track violations
    if user_id not in user_violations:
        user_violations[user_id] = 0

    if block_warning:
        user_violations[user_id] += 1

    if user_violations[user_id] >= 3:
        user_blocked_until[user_id] = current_time + 120  # 2-minute block
        user_violations[user_id] = 0  # Reset violations after block
        return jsonify({
            "blocked": True,
            "message": "You are blocked for 120 seconds."
        })

    return jsonify({
        "flagged": flagged,
        "block_warning": block_warning,
        "toxicity": toxicity,
        "blocked": False
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

