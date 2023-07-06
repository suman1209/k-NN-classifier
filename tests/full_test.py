from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd().parent))
from regressions.regression_test import run_regression  # noqa: E402
import subprocess  # noqa: E402
from classifier_classes.config import Config  # noqa: E402


if __name__ == "__main__":
    # setting the configs
    # initialising the configuration
    Config.CONFIG_JSON = "tests/classifier_config.json"
    # during the initialisation of the config class the reports directory will be emptied
    config = Config()
    run_regression()
    home_env_var = config.home_dir
    print("\n=========================== Running Unit Tests =============================")
    command = f'pytest {home_env_var}/tests/unittests/'
    subprocess.run(command, shell=True)
