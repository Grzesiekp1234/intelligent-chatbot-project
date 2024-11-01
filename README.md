# Intelligent Customer Support Chatbot

## Project Description

This project is an **Intelligent Customer Support Chatbot** designed to assist users by answering frequently asked questions (FAQs), tracking orders, handling user authentication, and providing advanced natural language responses using OpenAI's GPT-4. Built with FastAPI for a robust backend, containerized with Docker, and deployed on Microsoft Azure App Service, the chatbot leverages CI/CD pipelines via GitHub Actions to ensure seamless integration and deployment.

## Features

- **FAQ Handling:** Provides quick responses to common customer inquiries.
- **Order Tracking:** Allows users to track the status of their orders in real-time.
- **User Authentication:** Secure login system to manage user sessions and data.
- **Natural Language Processing:** Utilizes OpenAI GPT-4 for generating human-like responses.
- **Automated Testing:** Comprehensive test suites using `pytest` to ensure reliability.
- **Containerization:** Dockerized application for consistent environments across development and production.
- **CI/CD Pipeline:** Automated testing and deployment workflows with GitHub Actions.
- **Monitoring & Logging:** Integrated with Azure Application Insights for real-time monitoring and detailed logging.

## Technologies Used

- **Programming Language:** Python
- **Framework:** FastAPI
- **LLM Model:** OpenAI GPT-4
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud Platform:** Microsoft Azure App Service
- **Testing:** pytest
- **Version Control:** Git & GitHub
- **Monitoring:** Azure Application Insights

## Installation

### Prerequisites

- Python 3.8 or newer
- Git
- Docker
- Azure Account

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/intelligent-chatbot.git
    cd intelligent-chatbot
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    # Activate the virtual environment:
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**
    - Create a `.env` file in the project root:
      ```plaintext
      OPENAI_API_KEY=your_openai_api_key_here
      SECRET_KEY=your_secret_key_here
      APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string_here
      ```

5. **Run the Application Locally:**
    ```bash
    uvicorn main:app --reload
    ```
    - Access the chatbot at [http://localhost:8000/](http://localhost:8000/)
    - Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage

### Register a User

- **Current Users:**
  - Username: `john`
  - Password: `secret`

- **Obtain a Token:**
  ```bash
  curl -X POST "http://localhost:8000/token" -d "username=john&password=secret"
