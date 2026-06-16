from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.routes.health import router as health_router
from apps.api.routes.research_questions import router as research_questions_router
from research_copilot.core.config import get_settings
from research_copilot.core.logging import configure_logging, get_logger


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(settings.app_name)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        {
            "message": "api_startup",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
        }
    )
    yield


app = FastAPI(
    title="AI Research Copilot",
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(research_questions_router)
