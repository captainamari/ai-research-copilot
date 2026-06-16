from fastapi.testclient import TestClient

from apps.api.main import app
from research_copilot.services.health_service import get_health_status


def test_get_health_status() -> None:
    assert get_health_status() == {
        "status": "ok",
        "service": "ai-research-copilot",
        "version": "0.1.0",
    }


def test_health_endpoint_returns_status() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ai-research-copilot",
        "version": "0.1.0",
    }
