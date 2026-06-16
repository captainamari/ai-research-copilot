from research_copilot.services.health_service import get_health_status


def test_get_health_status() -> None:
    assert get_health_status() == {
        "status": "ok",
        "service": "ai-research-copilot",
    }
