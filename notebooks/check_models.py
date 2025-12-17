import google.generativeai as genai
import os
from dotenv import load_dotenv

# Loading ambient
load_dotenv("backend/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API Key not found on .env")
else:
    print(f"Key found: ...{api_key[-4:]}")
    genai.configure(api_key=api_key)

    print("\n---MODELS AVAILABLE FOR YOUR ACCOUNT---")
    try:
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}")
                found_any = True

        if not found_any:
            print("No text generation model was found. Check your key permissions")

    except Exception as e:
        print(f"Error while listing models: {e}")
