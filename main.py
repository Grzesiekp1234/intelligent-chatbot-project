from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class Message(BaseModel):
    user_id: str
    message: str

# Predefined FAQ responses
FAQ = {
    "how to register an account?": "To register an account, please go to the registration page and fill out the form.",
    "how to track my order?": "You can track your order by logging into your account and navigating to the 'My Orders' section.",
    # Add more FAQ entries as needed
}

def get_llm_response(user_message: str) -> str:
    """
    Fetch response from the LLM model or return FAQ answer if available.
    """
    normalized_message = user_message.lower()
    if normalized_message in FAQ:
        return FAQ[normalized_message]
    else:
        # Integrate with OpenAI GPT-4
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": user_message}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Sorry, there was an error processing your request."

@app.post("/chat/")
async def chat(message: Message):
    """
    Endpoint to handle chat messages from users.
    """
    response = get_llm_response(message.message)
    return {"response": response}
