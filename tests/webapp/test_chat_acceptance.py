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
    response = client.post("/api/chat/completion", json={
        "history": [
            {
                "role": "You",
                "content": "Was will die CDU für Einwanderer tun?"
            }
        ],
        "question": "Was will die CDU für Einwanderer tun?"
    },
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'answer' in response_json
    assert 'CDU' in response_json['answer']
    assert 'Einwanderer' or 'Einwanderung' in response_json['answer']


def tests_chat_party_inferred_from_history():
    response = client.post("/api/chat/completion", json={
        "history": [
            {
                "role": "You",
                "content": "Was denkt die CDU über die Wirtschaft?"
            },
            {
                "role": "AI",
                "content": "CDU will Plan X umsetzen"
            },
            {
                "role": "You",
                "content": "Was wollen sie für Einwanderer tun?"
            }
        ],
        "question": "Was wollen sie für Einwanderer tun?"
    },
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'answer' in response_json
    assert 'CDU' in response_json['answer']
    assert 'Einwanderer' or 'Einwanderung' in response_json['answer']


def tests_chat_doesnt_support_party():
    question = "Was wollen sie für Einwanderer tun?"
    response = client.post("/api/chat/completion", json={
        "history": [
            {
                "role": "You",
                "content": question
            }
        ],
        "question": question
    },
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 404

    response_json = response.json()

    error_detail = response_json['detail']
    print(error_detail)
    assert error_detail == ("Oops! Ich habe nicht verstanden, auf welche Partei sich deine Frage bezieht. "
                            "Bitte nenne eine der folgenden: SPD, CDU, AFD, FDP, DL, DG, BSW")


def tests_chatbot_understand_old_questions():
    question = "Was habe ich Sie in der vorherigen Frage gefragt?"
    response = client.post("/api/chat/completion", json={
        "history": [
            {
                "role": "You",
                "content": "Was will die CDU für die Wirtschaft tun?"
            },
            {
                "role": "AI",
                "content": "CDU will Plan X umsetzen"
            },
            {
                "role": "You",
                "content": question
            }
        ],
        "question": question
    },
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'economy' or 'CDU' in response_json['answer']


def tests_chat_returns_most_pertinent_chunks():
    response = client.post("/api/chat/retrieve", json={
        "question": "Was will die CDU für Einwanderer tun?"
    },
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'chunks' in response_json
    assert len(response_json['chunks']) == 4


def tests_chat_returns_only_cdu_chunks():
    response = client.post("/api/chat/retrieve", json={
        "question": "Was will die CDU für die Wirtschaft tun?"},
                           headers={"Authorization": f"Basic {basic_auth}"})

    assert response.status_code == 200

    response_json = response.json()

    chunks = response_json['chunks']
    assert len(chunks) > 0
    assert all('CDU' in chunk['text']['metadata']['source'] for chunk in chunks)
