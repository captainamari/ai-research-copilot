from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ResearchLogEntry(BaseModel):
    title: str
    content: str
    entry_type: Literal["note", "hypothesis", "evidence", "decision"] = "note"
    created_at: datetime = Field(default_factory=datetime.utcnow)
