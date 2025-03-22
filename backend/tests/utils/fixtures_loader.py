import json
from pathlib import Path


def load_fixture(filename: str) -> dict:
    """
    Load a JSON fixture from tests/utils/fixtures directory.
    """
    base_dir = Path(__file__).resolve().parent / "fixtures"
    path = base_dir / filename

    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)
