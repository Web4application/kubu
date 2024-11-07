import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/f1b68c5fdd45d470836192141029a324/ai/run/"
headers = {"Authorization": "Bearer {JxR1tnlcVpRxE4y3SnAtd8z1hOKdblQtBNmCBBn4}"}


def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    { "role": "system", "content": "You are a friendly assistan that helps write stories" },
    { "role": "user", "content": "Write a short story about a llama that goes on a journey to find an orange cloud "}
];
output = run("@cf/meta/llama-3-8b-instruct", inputs)
print(output)
