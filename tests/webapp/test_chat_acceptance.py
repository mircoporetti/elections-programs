import base64
import os

from fastapi.testclient import TestClient

from src.webapp.main import app
import pytest

from store import vector_store

client = TestClient(app)

username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")
basic_auth = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")


@pytest.fixture(scope="session", autouse=True)
def init_vector_store():
    vector_store.init()
    print("Vector store initialized")


def tests_chat_completion():
    response = client.post("/api/chat/completion", json={"query": "What CDU wants to do for immigrants?"},
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'answer' in response_json
    assert 'CDU' in response_json['answer']
    assert 'immigrants' in response_json['answer']


def tests_chat_returns_most_pertinent_chunks():
    response = client.post("/api/chat/retrieve", json={"query": "What CDU wants to do for immigrants?"},
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'chunks' in response_json
    assert len(response_json['chunks']) > 0
