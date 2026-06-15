from research_copilot.core.config import get_settings


def get_health_status() -> dict[str, str]:
    return {
        "status": "ok",
        "service": get_settings().app_name,
    }
