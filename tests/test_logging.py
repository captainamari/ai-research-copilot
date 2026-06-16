import logging

from research_copilot.core.logging import configure_logging, get_logger


def test_get_logger_writes_prefixed_structured_message(capsys) -> None:
    configure_logging(level="DEBUG")

    logger = get_logger("unit")
    logger.info({"message": "研究", "count": 2})

    output = capsys.readouterr().out
    assert output.startswith("[unit]")
    assert "[INFO]- " in output
    assert '"message": "研究"' in output
    assert '"count": 2' in output


def test_default_logger_uses_case_format(capsys) -> None:
    configure_logging(level="DEBUG")

    logger = get_logger()
    logger.info("ready")

    output = capsys.readouterr().out
    assert output.startswith("[case]")
    assert "[INFO]- ready" in output


def test_logger_level_can_be_changed(capsys) -> None:
    configure_logging(level="DEBUG")

    logger = get_logger("level")
    logger.setLevel(logging.ERROR)
    logger.info("hidden")
    logger.error("shown")

    output = capsys.readouterr().out
    assert "hidden" not in output
    assert "shown" in output
