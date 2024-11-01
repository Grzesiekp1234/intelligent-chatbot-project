import logging
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    user_id: str
    message: str

FAQ = {
    "how to register an account?": "To register an account, please go to the registration page and fill out the form.",
    # ... other FAQs
}

def get_llm_response(user_message: str) -> str:
    """
    Fetch response from the LLM model or return FAQ answer if available.
    """
    if not user_message.strip():
        logger.warning("Received empty message.")
        return "Please enter a valid message."

    normalized_message = user_message.lower()
    if normalized_message in FAQ:
        logger.info(f"FAQ matched for message: {user_message}")
        return FAQ[normalized_message]
    else:
        # Integrate with OpenAI GPT-4
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables.")
            return "Configuration error: API key is missing."

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4o-mini",
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

@app.post("/chat/")
async def chat(message: Message):
    """
    Endpoint to handle chat messages from users.
    """
    logger.info(f"Received message from user {message.user_id}: {message.message}")
    response = get_llm_response(message.message)
    logger.info(f"Responding to user {message.user_id} with: {response}")
    return {"response": response}

@app.get("/test-env")
async def test_env():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return {"status": "API key loaded successfully."}
    else:
        return {"status": "API key not found."}
