from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_and_chat() -> None:
    upload = client.post("/api/documents/upload", files={"file": ("notes.txt", b"FastAPI powers the VoxKnowledge backend.", "text/plain")})
    assert upload.status_code == 201
    response = client.post("/api/chat", json={"question": "What powers the backend?"})
    assert response.status_code == 200
    assert "FastAPI" in response.json()["answer"]
    assert response.json()["sources"]
