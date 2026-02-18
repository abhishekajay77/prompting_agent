import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    # Check if we can get it from Streamlit's secrets or env if set manually
    print("XAI_API_KEY not found in environment.")
    sys.exit(1)

print(f"Using API Key (first 4): {api_key[:4]}...")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    models = client.models.list()
    print("Successfully connected to xAI. Available models:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error listing models: {e}")
