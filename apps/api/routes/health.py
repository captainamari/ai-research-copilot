from fastapi import APIRouter

from research_copilot.services.health_service import get_health_status

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return get_health_status()
