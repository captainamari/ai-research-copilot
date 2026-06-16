from datetime import UTC, datetime
from uuid import uuid4

from research_copilot.research_os.schemas import (
    ResearchQuestion,
    ResearchQuestionCreate,
    ResearchQuestionStatusUpdate,
)
from research_copilot.research_os.storage import LocalJSONStorage


class ResearchQuestionService:
    def __init__(self, storage: LocalJSONStorage | None = None) -> None:
        self.storage = storage or LocalJSONStorage()

    def create_question(self, payload: ResearchQuestionCreate) -> ResearchQuestion:
        now = _utc_now()
        question = ResearchQuestion(
            id=f"rq_{uuid4().hex}",
            title=payload.title,
            description=payload.description,
            company=payload.company,
            theme=payload.theme,
            status="open",
            created_at=now,
            updated_at=now,
        )
        return self.storage.save(question)

    def list_questions(self) -> list[ResearchQuestion]:
        return self.storage.all(ResearchQuestion)

    def get_question(self, question_id: str) -> ResearchQuestion | None:
        return self.storage.get(ResearchQuestion, question_id)

    def update_question_status(
        self,
        question_id: str,
        payload: ResearchQuestionStatusUpdate,
    ) -> ResearchQuestion | None:
        return self.storage.update(
            ResearchQuestion,
            question_id,
            {
                "status": payload.status,
                "updated_at": _utc_now(),
            },
        )


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
