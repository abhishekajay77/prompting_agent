import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("No API key found")
else:
    client = Groq(api_key=api_key)
    models = client.models.list()
    for model in models.data:
        print(model.id)
