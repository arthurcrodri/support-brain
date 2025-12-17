import sys
import os
from dotenv import load_dotenv

# AMBIENT SETUP
# Adding backend root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Loading ambient variables
env_path = os.path.join(os.path.dirname(__file__), '../backend/.env')
load_dotenv(env_path)

from src.services.chat_service import ChatService

def test_chat():
    print("--- STARTING CHAT SERVICE TEST ---")

    try:
        # Instancing the service
        print("Initializing ChatService...")
        chat_service = ChatService()
        print("Service ready!")

        # Defining the question
        query = "O que eu faço se houver erro de temperatura?"
        print(f"User's input: '{query}'")

        # Calling ask() method
        print("Processing...")
        response = chat_service.ask(query)

        # Showing results
        print("\n--- AI MODEL RESPONSE ---")
        print(response['answer'])

        print("\n--- SOURCES USED ---")
        for source in response['sources']:
            print(f"- {source['source']} (Page {source['page']})")

        print(f"\nProcessing time: {response['processing_time']:.2f}s")
    except Exception as e:
        print(f"Error while testing: {e}")

if __name__ == "__main__":
    test_chat()
