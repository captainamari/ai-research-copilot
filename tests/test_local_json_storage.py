import json

from research_copilot.research_os.schemas import (
    Hypothesis,
    ResearchQuestion,
    ResearchSource,
)
from research_copilot.research_os.storage import LocalJSONStorage


def test_save_and_get_research_question(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    question = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        company="ACME",
        created_at="2026-06-16T04:00:00Z",
    )

    storage.save(question)

    assert storage.get(ResearchQuestion, "rq-1") == question
    assert storage.get(ResearchQuestion, "missing") is None


def test_all_returns_every_record_for_model(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    first = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        created_at="2026-06-16T04:00:00Z",
    )
    second = ResearchQuestion(
        id="rq-2",
        title="Will BETA revenue accelerate?",
        created_at="2026-06-16T04:01:00Z",
    )

    storage.save(first)
    storage.save(second)

    assert storage.all(ResearchQuestion) == [first, second]


def test_filter_returns_matching_records(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    acme_question = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        company="ACME",
        status="open",
        created_at="2026-06-16T04:00:00Z",
    )
    closed_acme_question = ResearchQuestion(
        id="rq-2",
        title="Did ACME execute the cost plan?",
        company="ACME",
        status="closed",
        created_at="2026-06-16T04:01:00Z",
    )
    beta_question = ResearchQuestion(
        id="rq-3",
        title="Will BETA revenue accelerate?",
        company="BETA",
        status="open",
        created_at="2026-06-16T04:02:00Z",
    )

    storage.save(acme_question)
    storage.save(closed_acme_question)
    storage.save(beta_question)

    assert storage.filter(ResearchQuestion, company="ACME", status="open") == [
        acme_question
    ]


def test_update_record_by_id(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    question = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        status="open",
        created_at="2026-06-16T04:00:00Z",
    )

    storage.save(question)
    updated = storage.update(
        ResearchQuestion,
        "rq-1",
        {"status": "closed", "updated_at": "2026-06-16T05:00:00Z"},
    )

    assert updated is not None
    assert updated.status == "closed"
    assert updated.updated_at == "2026-06-16T05:00:00Z"
    assert updated.id == "rq-1"
    assert storage.get(ResearchQuestion, "rq-1") == updated


def test_update_missing_record_returns_none(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)

    assert storage.update(ResearchQuestion, "missing", {"status": "closed"}) is None


def test_each_model_uses_a_separate_json_file(tmp_path) -> None:
    storage = LocalJSONStorage(tmp_path)
    question = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        created_at="2026-06-16T04:00:00Z",
    )
    hypothesis = Hypothesis(
        id="hyp-1",
        research_question_id="rq-1",
        content="Margins improve if cloud costs decline.",
        created_at="2026-06-16T04:01:00Z",
    )
    source = ResearchSource(
        id="src-1",
        filename="10k.pdf",
        source_type="filing",
        file_path="data/uploads/10k.pdf",
        uploaded_at="2026-06-16T04:02:00Z",
    )

    storage.save(question)
    storage.save(hypothesis)
    storage.save(source)

    assert json.loads((tmp_path / "research_questions.json").read_text()) == [
        question.model_dump(mode="json")
    ]
    assert json.loads((tmp_path / "hypotheses.json").read_text()) == [
        hypothesis.model_dump(mode="json")
    ]
    assert json.loads((tmp_path / "research_sources.json").read_text()) == [
        source.model_dump(mode="json")
    ]
    assert json.loads((tmp_path / "evidence_items.json").read_text()) == []
    assert json.loads((tmp_path / "research_logs.json").read_text()) == []
