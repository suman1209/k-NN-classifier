from pathlib import Path
import sys
home_env_var = str(Path.cwd().parent.parent)
sys.path.insert(0, home_env_var)


def test_dummy():
    assert 1 == 1, "Dummy test case failed"
