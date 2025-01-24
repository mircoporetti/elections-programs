from fastapi.testclient import TestClient

from src.webapp.main import app

client = TestClient(app)


def tests_programs_chat_returns_chunked_docs():
    response = client.post("/api/programs/chat", json={"query": "What CDU wants to do for immigrants?"})

    assert response.status_code == 200

    response_json = response.json()
    assert 'chunks' in response_json
    assert len(response_json['chunks']) > 0
