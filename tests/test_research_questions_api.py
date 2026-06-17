from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.routes.research_questions import get_research_question_service
from research_copilot.research_os.storage import LocalJSONStorage
from research_copilot.services.research_question_service import ResearchQuestionService


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    storage = LocalJSONStorage(tmp_path)

    def override_service() -> ResearchQuestionService:
        return ResearchQuestionService(storage)

    app.dependency_overrides[get_research_question_service] = override_service
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_research_question_api_flow(client: TestClient) -> None:
    create_response = client.post(
        "/research-questions",
        json={
            "title": "Is X-FAB undervalued for the AI era?",
            "description": "Research AI infrastructure and specialty foundry demand.",
            "company": "X-FAB",
            "theme": "AI infrastructure / specialty foundry",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"].startswith("rq_")
    assert created["title"] == "Is X-FAB undervalued for the AI era?"
    assert created["status"] == "open"
    assert created["company"] == "X-FAB"
    assert created["theme"] == "AI infrastructure / specialty foundry"
    assert created["created_at"].endswith("Z")
    assert created["updated_at"].endswith("Z")

    list_response = client.get("/research-questions")

    assert list_response.status_code == 200
    assert list_response.json() == [created]

    detail_response = client.get(f"/research-questions/{created['id']}")

    assert detail_response.status_code == 200
    assert detail_response.json() == created

    update_response = client.patch(
        f"/research-questions/{created['id']}",
        json={"status": "closed"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == created["id"]
    assert updated["status"] == "closed"
    assert updated["updated_at"].endswith("Z")

    missing_response = client.get("/research-questions/missing")

    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Research question not found"}


def test_research_question_create_validates_required_title(
    client: TestClient,
) -> None:
    response = client.post("/research-questions", json={"company": "X-FAB"})

    assert response.status_code == 422


def test_research_question_status_update_rejects_unknown_status(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/research-questions",
        json={"title": "Is X-FAB undervalued for the AI era?"},
    )
    created = create_response.json()

    response = client.patch(
        f"/research-questions/{created['id']}",
        json={"status": "paused"},
    )

    assert response.status_code == 422


def test_research_question_update_missing_id_returns_404(client: TestClient) -> None:
    response = client.patch("/research-questions/missing", json={"status": "closed"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Research question not found"}
