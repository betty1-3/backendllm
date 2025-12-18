import requests
import json

OPENROUTER_API_KEY = "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"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Debug Test"
}

payload = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "user", "content": "Say hello in one short sentence."}
    ],
    "temperature": 0.7,
    "max_tokens": 50
}

print("STARTING REQUEST...")

response = requests.post(API_URL, headers=headers, json=payload)

print("STATUS CODE:", response.status_code)
print("\nRAW RESPONSE TEXT:")
print(response.text)
