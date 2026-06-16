import pytest
from pydantic import ValidationError

from research_copilot.research_os.schemas import (
    EvidenceItem,
    Hypothesis,
    ResearchLog,
    ResearchQuestion,
    ResearchSource,
)


def test_research_question_can_be_initialized() -> None:
    question = ResearchQuestion(
        id="rq-1",
        title="Will ACME margins expand?",
        created_at="2026-06-16T04:00:00Z",
    )

    assert question.status == "open"
    assert question.description is None
    assert question.company is None
    assert question.theme is None
    assert question.updated_at is None


def test_research_question_status_is_validated() -> None:
    with pytest.raises(ValidationError):
        ResearchQuestion(
            id="rq-1",
            title="Will ACME margins expand?",
            status="paused",
            created_at="2026-06-16T04:00:00Z",
        )


def test_hypothesis_can_be_initialized() -> None:
    hypothesis = Hypothesis(
        id="hyp-1",
        research_question_id="rq-1",
        content="Margins improve if cloud costs decline.",
        created_at="2026-06-16T04:01:00Z",
    )

    assert hypothesis.status == "active"
    assert hypothesis.belief_before is None
    assert hypothesis.expected_evidence == []


def test_research_source_can_be_initialized() -> None:
    source = ResearchSource(
        id="src-1",
        filename="10k.pdf",
        source_type="filing",
        file_path="data/uploads/10k.pdf",
        uploaded_at="2026-06-16T04:02:00Z",
    )

    assert source.company is None
    assert source.year is None
    assert source.primary_source is False
    assert source.source_quality_score == 0.5


def test_evidence_item_can_be_initialized() -> None:
    evidence = EvidenceItem(
        id="ev-1",
        research_question_id="rq-1",
        source_id="src-1",
        chunk_id="chunk-1",
        evidence_type="supporting",
        content="Gross margin increased year over year.",
    )

    assert evidence.hypothesis_id is None
    assert evidence.strength_score is None
    assert evidence.source_quality_score is None
    assert evidence.citation is None


def test_research_log_can_be_initialized() -> None:
    log = ResearchLog(
        id="log-1",
        research_question_id="rq-1",
        query="Find gross margin trend.",
        created_at="2026-06-16T04:03:00Z",
    )

    assert log.hypothesis_id is None
    assert log.expectation is None
    assert log.observed_result is None
    assert log.belief_before is None
    assert log.belief_after is None
    assert log.lesson_learned is None
    assert log.next_actions == []


@pytest.mark.parametrize(
    ("schema_class", "payload"),
    [
        (ResearchQuestion, {"id": "rq-1", "created_at": "2026-06-16T04:00:00Z"}),
        (
            Hypothesis,
            {
                "id": "hyp-1",
                "research_question_id": "rq-1",
                "created_at": "2026-06-16T04:01:00Z",
            },
        ),
        (
            ResearchSource,
            {
                "id": "src-1",
                "filename": "10k.pdf",
                "source_type": "filing",
                "uploaded_at": "2026-06-16T04:02:00Z",
            },
        ),
        (
            EvidenceItem,
            {
                "id": "ev-1",
                "research_question_id": "rq-1",
                "source_id": "src-1",
                "chunk_id": "chunk-1",
                "evidence_type": "supporting",
            },
        ),
        (
            ResearchLog,
            {
                "id": "log-1",
                "research_question_id": "rq-1",
                "created_at": "2026-06-16T04:03:00Z",
            },
        ),
    ],
)
def test_required_fields_are_validated(schema_class, payload) -> None:
    with pytest.raises(ValidationError):
        schema_class(**payload)


def test_list_defaults_are_not_shared_between_instances() -> None:
    first_hypothesis = Hypothesis(
        id="hyp-1",
        research_question_id="rq-1",
        content="Margins improve.",
        created_at="2026-06-16T04:01:00Z",
    )
    second_hypothesis = Hypothesis(
        id="hyp-2",
        research_question_id="rq-1",
        content="Margins decline.",
        created_at="2026-06-16T04:02:00Z",
    )

    first_hypothesis.expected_evidence.append("10-K margin table")

    assert first_hypothesis.expected_evidence == ["10-K margin table"]
    assert second_hypothesis.expected_evidence == []

    first_log = ResearchLog(
        id="log-1",
        research_question_id="rq-1",
        query="Find margin data.",
        created_at="2026-06-16T04:03:00Z",
    )
    second_log = ResearchLog(
        id="log-2",
        research_question_id="rq-1",
        query="Find cost data.",
        created_at="2026-06-16T04:04:00Z",
    )

    first_log.next_actions.append("Check latest filing")

    assert first_log.next_actions == ["Check latest filing"]
    assert second_log.next_actions == []
