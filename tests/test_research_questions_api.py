from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.routes.research_questions import get_research_question_storage
from research_copilot.research_os.storage import LocalJSONStorage


def test_create_and_list_research_questions(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    app.dependency_overrides[get_research_question_storage] = lambda: storage
    client = TestClient(app)

    try:
        create_response = client.post(
            "/research-questions",
            json={
                "title": "Will ACME margins expand?",
                "description": "Track whether cost controls flow through.",
                "company": "ACME",
                "theme": "Margins",
            },
        )

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["id"].startswith("rq-")
        assert created["title"] == "Will ACME margins expand?"
        assert created["status"] == "open"

        list_response = client.get("/research-questions")

        assert list_response.status_code == 200
        assert list_response.json() == [created]
    finally:
        app.dependency_overrides.clear()


def test_create_research_question_requires_title(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    app.dependency_overrides[get_research_question_storage] = lambda: storage
    client = TestClient(app)

    try:
        response = client.post("/research-questions", json={"title": "   "})

        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()
