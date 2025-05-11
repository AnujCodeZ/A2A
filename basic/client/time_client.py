import requests
import uuid

base_url = "http://localhost:5001"

res = requests.get(f"{base_url}/.well-known/agent.json")

if res.status_code != 200:
    raise Exception("Failed to discover agent.")

agent_info = res.json()

print(f"Connected to {agent_info['name']} - {agent_info['description']}")

task_id = str(uuid.uuid4())

task_payload = {
    "id": task_id,
    "message": {
        "role": "user",
        "parts": [{"text": "What time is it?"}]
    }
}

response = requests.post(f"{base_url}/tasks/send", json=task_payload)

if response.status_code != 200:
    raise Exception(f"Task failed: {response.text}")

response_data = response.json()

messages = response_data.get("messages", [])

if messages:
    final_reply = messages[-1]["parts"][0]["text"]
    print(f"Agent reply: {final_reply}")
else:
    raise Exception("No response from agent.")
