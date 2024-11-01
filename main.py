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

# Pydantic model for incoming messages
class Message(BaseModel):
    message: str

# Function to fetch response from the chosen OpenAI model
def get_llm_response(user_message: str) -> str:
    """
    Fetch response from the chosen OpenAI model.
    """
    if not user_message.strip():
        logger.warning("Received empty message.")
        return "Please enter a valid message."

    # Simple keyword-based responses for Help/FAQ redirection
    if "help" in user_message.lower() or "faq" in user_message.lower():
        return (
            "Sure! Please visit our [Help Page](http://yourdomain.com/help) "
            "or check out our [FAQ](http://yourdomain.com/faq) for more information."
        )

    # Integrate with the chosen OpenAI model (e.g., "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables.")
        return "Configuration error: API key is missing."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",  # Define openai model 
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