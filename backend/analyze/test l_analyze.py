import requests

url = "http://localhost:8000/analyze"  # Change if your server runs elsewhere

payload = {
    "file": "console.log('hello world');"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.ok:
    print("Response from server:")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
