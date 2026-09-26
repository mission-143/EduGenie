from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation():
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422


def test_security_headers():
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_ai_failure_returns_json_error(monkeypatch):
    from ai_service import AIServiceError

    def fail(_question):
        raise AIServiceError("GEMINI_API_KEY is not configured.")

    monkeypatch.setattr(main, "answer_question", fail)
    response = client.post("/qa", json={"question": "What is gravity?"})
    assert response.status_code == 503
    assert "GEMINI_API_KEY" not in response.json()["detail"]
