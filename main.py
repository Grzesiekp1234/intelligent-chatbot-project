# main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the FAQ dictionary
FAQ = {
    "how to register an account?": "To register an account, please go to the registration page and fill out the form.",
    "how to track my order?": "You can track your order by logging into your account and navigating to the 'My Orders' section.",
    "what is your return policy?": "Our return policy allows returns within 30 days of purchase with a valid receipt.",
    "how to contact support?": "You can contact support by emailing support@yourcompany.com or calling 1-800-123-4567.",
    "what payment methods do you accept?": "We accept Visa, MasterCard, American Express, and PayPal.",
    "how do i reset my password?": "To reset your password, click on 'Forgot Password' on the login page and follow the instructions.",
    # Add more as needed
}

# Pydantic model for incoming messages
class Message(BaseModel):
    message: str

def get_llm_response(user_message: str) -> str:
    """
    Fetch response from the LLM model or return FAQ answer if available.
    """
    if not user_message.strip():
        logger.warning("Received empty message.")
        return "Please enter a valid message."

    # Normalize the user message
    normalized_message = user_message.strip().lower()
    
    # Check if the normalized message is in FAQ
    if normalized_message in FAQ:
        logger.info(f"FAQ matched for message: {user_message}")
        return FAQ[normalized_message]

    # If not an FAQ, fetch response from the OpenAI model
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables.")
        return "Configuration error: API key is missing."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",  # Chose the model here
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        llm_response = response.json()['choices'][0]['message']['content']
        logger.info(f"LLM response: {llm_response}")
        return llm_response
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return "Sorry, there was an error processing your request."
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        return "Sorry, there was an error processing your request."
    except KeyError as key_err:
        logger.error(f"Unexpected response structure: {key_err} - Response: {response.text}")
        return "Sorry, there was an error processing your request."

# Endpoint to handle chat messages from users
@app.post("/chat/")
def chat(message: Message):
    """
    Endpoint to handle chat messages from users.
    """
    logger.info(f"Received message: {message.message}")
    response = get_llm_response(message.message)
    logger.info(f"Responding with: {response}")
    return {"response": response}

 # Serve the homepage with the chatbot interface
@app.get("/", response_class=HTMLResponse)
async def get_home():
    """
    Serve the homepage with the chatbot interface.
    """
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Test endpoint to check if the API key is loaded
@app.get("/test-env")
async def test_env():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return {"status": "API key loaded successfully."}
    else:
        return {"status": "API key not found."}