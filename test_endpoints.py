"""Test both LangSmith endpoints to see which one actually works."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LANGSMITH_API_KEY")
project = os.getenv("LANGSMITH_PROJECT", "test")

headers = {
    "x-api-key": api_key,
    "Langsmith-Project": project,
    "Content-Type": "application/x-protobuf"
}

# Test data (minimal OTLP trace)
test_data = b'\n\x00'  # Empty but valid protobuf

endpoints = [
    "https://api.smith.langchain.com/otel/v1/traces",
    "https://api.smith.langchain.com:443/otel/v1/traces"
]

for endpoint in endpoints:
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.post(endpoint, headers=headers, data=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")