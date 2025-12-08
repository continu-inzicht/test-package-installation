import pytest
from pathlib import Path
import sys

def run_tests(dir):
    path = Path(__file__).parent / "tests/src"
    if dir == "all":
        pass
    else:   
        path = path /  dir
    pytest.main([str(path), "-v"])


if __name__ == "__main__":
    run_tests(sys.argv[1])