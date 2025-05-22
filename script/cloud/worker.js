import os
import requests

ACCOUNT_ID = "3c2d8a9226729b067992b8515d7c2a75"
AUTH_TOKEN = os.environ.get("aVZM8HSx1|rFNqUj7Zmo_3ZkAMUwxju|4QUHcStS")

prompt = "Tell me all about PEP-8"
response = requests.post(
  f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@hf/nousresearch/hermes-2-pro-mistral-7b",
    headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
    json={
      "messages": [
        {"role": "system", "content": "You are a friendly assistant"},
        {"role": "user", "content": prompt}
      ]
    }
)
result = response.json()
print(result)
