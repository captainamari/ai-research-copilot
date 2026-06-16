from fastapi import APIRouter, Depends, HTTPException, status

from research_copilot.research_os.schemas import (
    ResearchQuestion,
    ResearchQuestionCreate,
    ResearchQuestionStatusUpdate,
)
from research_copilot.services.research_question_service import ResearchQuestionService


router = APIRouter(prefix="/research-questions", tags=["research-questions"])


def get_research_question_service() -> ResearchQuestionService:
    return ResearchQuestionService()


@router.post("", response_model=ResearchQuestion, status_code=status.HTTP_201_CREATED)
def create_research_question(
    payload: ResearchQuestionCreate,
    service: ResearchQuestionService = Depends(get_research_question_service),
) -> ResearchQuestion:
    return service.create_question(payload)


@router.get("", response_model=list[ResearchQuestion])
def list_research_questions(
    service: ResearchQuestionService = Depends(get_research_question_service),
) -> list[ResearchQuestion]:
    return service.list_questions()


@router.get("/{question_id}", response_model=ResearchQuestion)
def get_research_question(
    question_id: str,
    service: ResearchQuestionService = Depends(get_research_question_service),
) -> ResearchQuestion:
    question = service.get_question(question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research question not found",
        )
    return question


@router.patch("/{question_id}", response_model=ResearchQuestion)
def update_research_question_status(
    question_id: str,
    payload: ResearchQuestionStatusUpdate,
    service: ResearchQuestionService = Depends(get_research_question_service),
) -> ResearchQuestion:
    question = service.update_question_status(question_id, payload)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research question not found",
        )
    return question
