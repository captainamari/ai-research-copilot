from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator

from research_copilot.research_os.schemas import ResearchQuestion
from research_copilot.research_os.storage import LocalJSONStorage


router = APIRouter(prefix="/research-questions", tags=["research-questions"])


class ResearchQuestionCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    company: str | None = None
    theme: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title is required")
        return value

    @field_validator("description", "company", "theme")
    @classmethod
    def empty_strings_become_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


def get_research_question_storage() -> LocalJSONStorage:
    return LocalJSONStorage()


StorageDependency = Annotated[LocalJSONStorage, Depends(get_research_question_storage)]


@router.get("", response_model=list[ResearchQuestion])
def list_research_questions(storage: StorageDependency) -> list[ResearchQuestion]:
    return sorted(
        storage.all(ResearchQuestion),
        key=lambda question: question.created_at,
        reverse=True,
    )


@router.post("", response_model=ResearchQuestion, status_code=201)
def create_research_question(
    payload: ResearchQuestionCreate,
    storage: StorageDependency,
) -> ResearchQuestion:
    now = datetime.now(UTC).isoformat()
    question = ResearchQuestion(
        id=f"rq-{uuid4()}",
        title=payload.title,
        description=payload.description,
        company=payload.company,
        theme=payload.theme,
        status="open",
        created_at=now,
        updated_at=now,
    )
    return storage.save(question)
