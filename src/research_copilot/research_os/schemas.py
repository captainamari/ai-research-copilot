from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ResearchQuestion(BaseModel):
    id: str
    title: str
    description: str | None = None
    company: str | None = None
    theme: str | None = None
    status: str = "open"
    created_at: str
    updated_at: str | None = None


class Hypothesis(BaseModel):
    id: str
    research_question_id: str
    content: str
    belief_before: float | None = None
    expected_evidence: list[str] = Field(default_factory=list)
    status: str = "active"
    created_at: str


class ResearchSource(BaseModel):
    id: str
    filename: str
    source_type: str
    file_path: str
    company: str | None = None
    year: int | None = None
    primary_source: bool = False
    source_quality_score: float = 0.5
    uploaded_at: str


class EvidenceItem(BaseModel):
    id: str
    research_question_id: str
    hypothesis_id: str | None = None
    source_id: str
    chunk_id: str
    evidence_type: str
    content: str
    strength_score: float | None = None
    source_quality_score: float | None = None
    citation: str | None = None


class ResearchLog(BaseModel):
    id: str
    research_question_id: str
    hypothesis_id: str | None = None
    query: str
    expectation: str | None = None
    observed_result: str | None = None
    belief_before: float | None = None
    belief_after: float | None = None
    lesson_learned: str | None = None
    next_actions: list[str] = Field(default_factory=list)
    created_at: str


class ResearchLogEntry(BaseModel):
    title: str
    content: str
    entry_type: Literal["note", "hypothesis", "evidence", "decision"] = "note"
    created_at: datetime = Field(default_factory=datetime.utcnow)
