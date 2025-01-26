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
    assert len(response_json['chunks']) == 4


def tests_chat_returns_only_CDU_chunks():
    response = client.post("/api/chat/retrieve", json={"query": "What CDU wants to do for economy?"},
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()

    chunks = response_json['chunks']
    assert len(chunks) > 0
    assert all('CDU' in chunk['text']['metadata']['source'] for chunk in chunks)


def tests_chat_doesnt_support_party():
    question = "What do my favorite party wants to do for economy?"
    response = client.post("/api/chat/retrieve", json={"query": question},
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 404

    response_json = response.json()

    error_detail = response_json['detail']
    assert error_detail == (f"The provided question '{question}' does not "
                            "reference any supported political party. Please include one of the following: SPD, CDU")


