# Intelligent Customer Support Chatbot

## Project Description

The **Intelligent Customer Support Chatbot** is a robust and scalable solution designed to assist users by answering frequently asked questions (FAQs) and providing advanced natural language responses using OpenAI's GPT-4o-mini model. Built with **FastAPI** for a high-performance backend and a responsive frontend interface, the chatbot is containerized with **Docker**, ensuring consistency across different environments and simplifying deployment.

## Features

- **FAQ Handling:**
  - Provides quick responses to common customer inquiries using a predefined FAQ system.
  - Reduces reliance on the OpenAI model for repetitive questions, enhancing efficiency and reducing costs.

- **Natural Language Processing:**
  - Utilizes OpenAI GPT-4o-mini for generating human-like responses to complex queries.

- **Normalized FAQ Responses:**
  - Implements a normalized FAQ system to handle user queries consistently, regardless of input variations.

- **Automated Testing:**
  - Comprehensive test suites using `pytest` ensure reliability and correctness of chatbot functionalities.
  - Tests cover FAQ responses, OpenAI model integrations, and edge cases.

- **Responsive Design:**
  - Frontend interface adapts seamlessly to various screen sizes and devices, including desktops, tablets, and mobile phones.

- **Formatted Responses:**
  - Parses and renders Markdown in chatbot responses for enhanced readability, including bold text, lists, and links.

- **Auto-Scrolling:**
  - Automatically scrolls to the latest message for a smooth and uninterrupted user experience.

- **Containerization:**
  - Dockerized application ensures consistent environments across development and production.
  - Simplifies deployment and scalability.

## Technologies Used

- **Programming Language:** Python
- **Framework:** FastAPI
- **LLM Model:** OpenAI GPT-4o-mini
- **Frontend:** HTML, CSS, JavaScript, Marked.js, DOMPurify
- **Containerization:** Docker, Docker Compose
- **Testing:** pytest, httpx
- **Version Control:** Git & GitHub

## Installation

### Prerequisites

- **Python:** Version 3.8 or newer
- **Git:** For version control
- **Docker:** For containerization
- **Docker Compose:** (Optional) For managing multi-container setups

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/YOUR_USERNAME/intelligent-chatbot.git
    cd intelligent-chatbot
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

    - **Activate the Virtual Environment:**
      - **Windows:**
        ```bash
        venv\Scripts\activate
        ```
      - **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3. **Install Dependencies:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    - **Create a `.env` File:**

        ```bash
        cp .env.example .env
        ```

    - **Edit the `.env` File:**

        Open the `.env` file in your preferred text editor and fill in the required environment variables:

        ```env
        OPENAI_API_KEY=your_openai_api_key_here
        SECRET_KEY=your_secret_key_here  # Optional
        APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string_here  # Optional, for monitoring
        ```

    **Important:** Ensure that the `.env` file is **not** committed to version control to protect sensitive information. The `.gitignore` is configured to exclude it.

5. **Run the Application Locally:**

    ```bash
    uvicorn main:app --reload
    ```

    - **Access the Chatbot Interface:**
      - Navigate to [http://localhost:8000/](http://localhost:8000/) in your web browser.
    - **Access Swagger UI:**
      - Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view and interact with the API documentation.

## Docker Setup

Containerizing your application ensures consistency across different environments and simplifies deployment.

### 1. **Build the Docker Image**

Navigate to the project root directory and build the Docker image:

```bash
docker build -t intelligent-chatbot:latest .
