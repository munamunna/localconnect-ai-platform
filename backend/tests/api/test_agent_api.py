from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import agent


client = TestClient(app)


def test_agent_chat_success(monkeypatch):
    def mock_run_agent(query: str, limit: int = 5):
        return {
            "message": "I found 1 freelancer matching your request.",
            "freelancers": [],
        }

    monkeypatch.setattr(
    agent,
    "run_agent",
    mock_run_agent,
    )

    response = client.post(
        "/api/agent/chat",
        json={
            "message": "Find me a plumber in Kozhikode",
        },
    )

    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["response"]["message"] == (
        "I found 1 freelancer matching your request."
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"]["message"] == (
        "I found 1 freelancer matching your request."
    )


def test_agent_chat_empty_message():
    response = client.post(
        "/api/agent/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Query is required"