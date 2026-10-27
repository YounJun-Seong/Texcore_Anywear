import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from safety_engine import load_rules  # noqa: E402


@pytest.fixture(scope="session")
def rules():
    return load_rules()
