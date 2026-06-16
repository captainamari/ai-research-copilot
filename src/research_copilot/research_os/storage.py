from pathlib import Path

from research_copilot.core.config import get_settings


def get_storage_dir() -> Path:
    storage_dir = get_settings().data_dir / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir
