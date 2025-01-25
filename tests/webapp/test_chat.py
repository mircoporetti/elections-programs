from fastapi.testclient import TestClient

from src.webapp.main import app
import pytest

from store import vector_store

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def init_vector_store():
    vector_store.init_vector_store()
    print("Vector store initialized")


def tests_chat_completion():
    response = client.post("/api/chat/completion", json={"query": "What CDU wants to do for immigrants?"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'answer' in response_json
    assert len(response_json['answer']) > 0


def tests_chat_returns_most_pertinent_chunks():
    response = client.post("/api/chat/retrieve", json={"query": "What CDU wants to do for immigrants?"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'chunks' in response_json
    assert len(response_json['chunks']) > 0
