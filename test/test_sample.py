import os
import sys
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))


import pytest



@pytest.mark.parametrize(('a', 'b', 'expected'), [
    (1, 1, 2),
])
def test_add(a, b, expected):
    assert (a + b) == expected