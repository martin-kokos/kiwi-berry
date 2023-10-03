import pytest

from pathlib import Path

import kiwi_berry

root = Path(kiwi_berry.__file__)


@pytest.fixture
def shared_datadir():
    return root.parent.parent / 'tests' / 'data'
