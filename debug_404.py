"""Debug the original 404 error by testing different header configurations."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LANGSMITH_API_KEY")
project = os.getenv("LANGSMITH_PROJECT", "test")

# Test data (minimal OTLP trace)
test_data = b'\n\x00'

endpoint = "https://api.smith.langchain.com/otel/v1/traces"

# Original problematic headers (from customer complaint)
original_headers = {
    'x-api-key': api_key,  # This was likely 'X-API-Key' or similar
    'Langsmith-Project': project  # Case sensitive?
}

# Alternative header variations that might cause 404
test_cases = [
    ("Original (working)", {
        'x-api-key': api_key,
        'Langsmith-Project': project,
        'Content-Type': 'application/x-protobuf'
    }),
    ("Wrong case X-API-Key", {
        'X-API-Key': api_key,  # Wrong case
        'Langsmith-Project': project,
        'Content-Type': 'application/x-protobuf'
    }),
    ("Wrong case LangSmith-Project", {
        'x-api-key': api_key,
        'LangSmith-Project': project,  # Different case
        'Content-Type': 'application/x-protobuf'
    }),
    ("Missing Content-Type", {
        'x-api-key': api_key,
        'Langsmith-Project': project
        # No Content-Type
    }),
    ("Wrong API Key header name", {
        'Authorization': f'Bearer {api_key}',  # Wrong auth method
        'Langsmith-Project': project,
        'Content-Type': 'application/x-protobuf'
    })
]

for name, headers in test_cases:
    print(f"\nTesting: {name}")
    print(f"Headers: {headers}")
    try:
        response = requests.post(endpoint, headers=headers, data=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("🚨 FOUND THE 404!")
        print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"Error: {e}")