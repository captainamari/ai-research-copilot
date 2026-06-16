import io
import json
import logging
import logging.config
import sys
from typing import Any

from research_copilot.core.config import get_settings

_LOGGER_NAME = "prefix"
_CASE_LOGGER_NAME = "case"
_DEFAULT_PREFIX = "case"
_SYSTEM_PREFIX = "ai-research-copilot"

_PREFIX_RED = "\033[0;31m"
_PREFIX_GREEN = "\033[0;32m"
_PREFIX_YELLOW = "\033[0;33m"
_PREFIX_DEFAULT = "\033[0m"


class _PrefixFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "prefix"):
            record.prefix = "none"
        return True


class _PrefixLogger(logging.LoggerAdapter):
    """Logger adapter that adds a stable prefix and formats structured values."""

    def process(
        self, msg: object, kwargs: dict[str, Any]
    ) -> tuple[object, dict[str, Any]]:
        extra = dict(self.extra or {})
        extra.update(kwargs.get("extra") or {})
        extra.setdefault("prefix", "none")
        kwargs["extra"] = extra
        return self.format(msg), kwargs

    def setLevel(self, level: int | str) -> None:  # noqa: N802 - match logging API
        self.logger.setLevel(level)

    @staticmethod
    def format(msg: object) -> object:
        if hasattr(msg, "x_raw"):
            return msg.x_raw()

        if isinstance(msg, (dict, list, tuple)):
            try:
                return json.dumps(
                    msg,
                    indent=2,
                    separators=(",", ": "),
                    skipkeys=True,
                    ensure_ascii=False,
                )
            except (TypeError, ValueError):
                return msg

        return msg

    def red_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.info(f"{_PREFIX_RED}{msg}{_PREFIX_DEFAULT}", *args, **kwargs)

    def green_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.info(f"{_PREFIX_GREEN}{msg}{_PREFIX_DEFAULT}", *args, **kwargs)

    def yellow_info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.info(f"{_PREFIX_YELLOW}{msg}{_PREFIX_DEFAULT}", *args, **kwargs)

    def red_error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.error(f"{_PREFIX_RED}{msg}{_PREFIX_DEFAULT}", *args, **kwargs)


def _ensure_stdout_utf8() -> None:
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding and encoding.lower().replace("-", "") == "utf8":
        return

    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        sys.stdout = io.TextIOWrapper(buffer, encoding="utf-8")


def configure_logging(level: int | str | None = None) -> None:
    settings = get_settings()
    log_level = level or settings.log_level

    _ensure_stdout_utf8()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "prefix": {
                    "()": _PrefixFilter,
                }
            },
            "formatters": {
                "standard": {
                    "format": (
                        "[%(prefix)s]%(asctime)s[%(filename)s:%(lineno)d]"
                        "[%(process)d][%(levelname)s]- %(message)s"
                    )
                },
                "simple": {
                    "format": "[%(prefix)s][%(levelname)s] %(message)s",
                },
                "case_custom": {
                    "format": (
                        "[case]%(asctime)s[%(filename)s:%(lineno)d]"
                        "[%(process)d][%(levelname)s]- %(message)s"
                    )
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "filters": ["prefix"],
                    "stream": "ext://sys.stdout",
                },
                "case_console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "case_custom",
                    "filters": ["prefix"],
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                _LOGGER_NAME: {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                },
                _CASE_LOGGER_NAME: {
                    "handlers": ["case_console"],
                    "level": log_level,
                    "propagate": False,
                },
            },
        }
    )


def get_logger(prefix: str | None = None) -> _PrefixLogger:
    logger = logging.getLogger(_LOGGER_NAME if prefix else _CASE_LOGGER_NAME)
    return _PrefixLogger(logger, {"prefix": prefix or _DEFAULT_PREFIX})


def set_system_log_level(level: int | str) -> None:
    get_logger(_SYSTEM_PREFIX).setLevel(level)
    logging.getLogger(_CASE_LOGGER_NAME).setLevel(level)


configure_logging()
