from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():
    return jsonify({
        "name": "Tell Time Agent",
        "description": "A simple agent that tells the current time",
        "url": "https://localhost:5001",
        "version": "1.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": ["tell_time"],
    })

@app.route("/tasks/send", methods=["POST"])
def handle_task():
    try:
        task = request.get_json()

        task_id = task.get("id")

        user_message = task["message"]["parts"][0]["text"]

    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "Invalid task format"}), 400
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    reply_text = f"The current time is: {current_time}"

    return jsonify({
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task["message"],
            {
                "role": "agent",
                "parts": [{"text": reply_text}]
            }
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
