import json
from pathlib import Path
from typing import Any


class StorageService:
    """Persists app state to a JSON file."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any] | None:
        if not self.file_path.exists():
            return None
        try:
            with self.file_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, data: dict[str, Any]) -> None:
        with self.file_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
