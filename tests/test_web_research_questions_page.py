from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from research_copilot.core.config import get_settings


PAGE_PATH = Path("apps/web/pages/1_Research_Questions.py")


def load_page_module():
    spec = spec_from_file_location("research_questions_page", PAGE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_api_url_uses_configured_base_url(monkeypatch) -> None:
    monkeypatch.setenv("API_BASE_URL", "http://api.example.test/")
    get_settings.cache_clear()
    page = load_page_module()

    try:
        assert page.api_url("/research-questions") == (
            "http://api.example.test/research-questions"
        )
    finally:
        get_settings.cache_clear()


def test_normalize_optional_strips_empty_values() -> None:
    page = load_page_module()

    assert page.normalize_optional("  ACME  ") == "ACME"
    assert page.normalize_optional("   ") is None
