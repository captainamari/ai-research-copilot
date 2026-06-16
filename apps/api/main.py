from fastapi import FastAPI

from research_copilot.services.health_service import get_health_status

app = FastAPI(title="AI Research Copilot")


@app.get("/health")
def health() -> dict[str, str]:
    return get_health_status()
