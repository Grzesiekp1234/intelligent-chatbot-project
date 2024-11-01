# tests/test_chatbot.py

import pytest
from fastapi.testclient import TestClient
from main import app, FAQ

client = TestClient(app)

# Fixture for TestClient
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def test_faq_responses(test_client):
    """
    Test that the chatbot returns the correct FAQ responses.
    """
    for question, answer in FAQ.items():
        response = test_client.post("/chat/", json={"message": question})
        assert response.status_code == 200
        assert response.json()["response"] == answer

def test_faq_responses_case_insensitive(test_client):
    """
    Test that the chatbot handles case-insensitive FAQ questions.
    """
    for question, answer in FAQ.items():
        # Capitalize the first letter of each word
        formatted_question = question.title()
        response = test_client.post("/chat/", json={"message": formatted_question})
        assert response.status_code == 200
        assert response.json()["response"] == answer

def test_non_faq_response(test_client, monkeypatch):
    """
    Test that the chatbot fetches a response from the OpenAI model when the question is not in FAQ.
    We'll mock the OpenAI API response to control the output.
    """
    mock_response = {
        "choices": [{
            "message": {
                "content": "This is a mocked response from the OpenAI model."
            }
        }]
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self._json = json_data
                self.status_code = status_code

            def json(self):
                return self._json

            def raise_for_status(self):
                if self.status_code != 200:
                    raise requests.HTTPError("Mocked error")

        return MockResponse(mock_response, 200)

    monkeypatch.setattr("requests.post", mock_post)

    response = test_client.post("/chat/", json={"message": "Tell me something interesting."})
    assert response.status_code == 200
    assert response.json()["response"] == "This is a mocked response from the OpenAI model."

def test_empty_message(test_client):
    """
    Test that the chatbot handles empty messages appropriately.
    """
    response = test_client.post("/chat/", json={"message": ""})
    assert response.status_code == 200
    assert response.json()["response"] == "Please enter a valid message."

def test_unknown_faq(test_client, monkeypatch):
    """
    Test that the chatbot fetches a response from the OpenAI model when the FAQ does not have an answer.
    We'll mock the OpenAI API response to control the output.
    """
    mock_response = {
        "choices": [{
            "message": {
                "content": "Here's a response from the OpenAI model for an unknown question."
            }
        }]
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self._json = json_data
                self.status_code = status_code

            def json(self):
                return self._json

            def raise_for_status(self):
                if self.status_code != 200:
                    raise requests.HTTPError("Mocked error")

        return MockResponse(mock_response, 200)

    monkeypatch.setattr("requests.post", mock_post)

    unknown_question = "What is the meaning of life?"
    response = test_client.post("/chat/", json={"message": unknown_question})
    assert response.status_code == 200
    assert response.json()["response"] == "Here's a response from the OpenAI model for an unknown question."
