import json
from pathlib import Path
from typing import Any, TypeAlias, TypeVar

from pydantic import BaseModel

from research_copilot.core.config import get_settings
from research_copilot.research_os.schemas import (
    EvidenceItem,
    Hypothesis,
    ResearchLog,
    ResearchQuestion,
    ResearchSource,
)


ResearchRecord: TypeAlias = (
    ResearchQuestion | Hypothesis | ResearchSource | EvidenceItem | ResearchLog
)
ResearchRecordT = TypeVar("ResearchRecordT", bound=ResearchRecord)


MODEL_FILE_NAMES: dict[type[ResearchRecord], str] = {
    ResearchQuestion: "research_questions.json",
    Hypothesis: "hypotheses.json",
    ResearchSource: "research_sources.json",
    EvidenceItem: "evidence_items.json",
    ResearchLog: "research_logs.json",
}


def get_storage_dir() -> Path:
    storage_dir = get_settings().data_dir / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


class LocalJSONStorage:
    """Local JSON-backed storage for MVP Research OS records."""

    def __init__(self, storage_dir: Path | None = None) -> None:
        self.storage_dir = storage_dir or get_storage_dir()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_files()

    def save(self, record: ResearchRecordT) -> ResearchRecordT:
        records = self._read_records(type(record))
        payload = self._dump_record(record)
        updated_records = [
            payload if existing["id"] == record.id else existing for existing in records
        ]

        if not any(existing["id"] == record.id for existing in records):
            updated_records.append(payload)

        self._write_records(type(record), updated_records)
        return record

    def get(
        self, model_class: type[ResearchRecordT], record_id: str
    ) -> ResearchRecordT | None:
        for record in self.all(model_class):
            if record.id == record_id:
                return record
        return None

    def all(self, model_class: type[ResearchRecordT]) -> list[ResearchRecordT]:
        return [
            model_class.model_validate(record)
            for record in self._read_records(model_class)
        ]

    def filter(
        self, model_class: type[ResearchRecordT], **criteria: Any
    ) -> list[ResearchRecordT]:
        return [
            record
            for record in self.all(model_class)
            if all(
                getattr(record, field, None) == value
                for field, value in criteria.items()
            )
        ]

    def update(
        self,
        model_class: type[ResearchRecordT],
        record_id: str,
        updates: dict[str, Any],
    ) -> ResearchRecordT | None:
        records = self._read_records(model_class)
        updated_record: ResearchRecordT | None = None

        updated_records = []
        for record in records:
            if record["id"] != record_id:
                updated_records.append(record)
                continue

            updated_payload = {**record, **updates, "id": record_id}
            updated_record = model_class.model_validate(updated_payload)
            updated_records.append(self._dump_record(updated_record))

        if updated_record is None:
            return None

        self._write_records(model_class, updated_records)
        return updated_record

    def _ensure_files(self) -> None:
        for file_name in MODEL_FILE_NAMES.values():
            path = self.storage_dir / file_name
            if not path.exists():
                path.write_text("[]\n", encoding="utf-8")

    def _get_path(self, model_class: type[ResearchRecord]) -> Path:
        try:
            return self.storage_dir / MODEL_FILE_NAMES[model_class]
        except KeyError as exc:
            raise ValueError(f"Unsupported model class: {model_class!r}") from exc

    def _read_records(self, model_class: type[ResearchRecord]) -> list[dict[str, Any]]:
        path = self._get_path(model_class)
        if not path.exists():
            return []

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Storage file contains invalid JSON: {path}") from exc

        if not isinstance(payload, list):
            raise ValueError(f"Storage file must contain a JSON array: {path}")

        for item in payload:
            if not isinstance(item, dict):
                raise ValueError(f"Storage records must be JSON objects: {path}")

        return payload

    def _write_records(
        self, model_class: type[ResearchRecord], records: list[dict[str, Any]]
    ) -> None:
        path = self._get_path(model_class)
        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        temp_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temp_path.replace(path)

    @staticmethod
    def _dump_record(record: BaseModel) -> dict[str, Any]:
        return record.model_dump(mode="json")
