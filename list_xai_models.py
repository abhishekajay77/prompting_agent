import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    print("No API key found in .env")
else:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    models = client.models.list()
    for model in models.data:
        print(model.id)
