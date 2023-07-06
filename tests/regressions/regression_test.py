from pathlib import Path
import os
import sys
sys.path.insert(0, str(Path.cwd().parent.parent))
from classifier_classes.config import Config  # noqa: E402
import subprocess  # noqa: E402
from classifier_classes.utilities import compare_two_files  # noqa: E402


def run_regression():
    # initialising the configuration
    Config.CONFIG_JSON = "tests/classifier_config.json"
    # during the initialisation of the config class the reports directory will be emptied
    config = Config()

    # change the current working directory to home_env_var
    home_env_var = config.home_dir
    os.chdir(home_env_var)
    print("### Deleted previous outputs ###")

    print("### Running the Application ###")
    # command you want to run
    command = ["python", "knn_classifier.py",
               "--raw_inp_data_path", "Dataset/iris_data.csv"]

    # Save the output from the subprocess to a file
    out_console_file_path = f"{config.report_dir}/console_output.txt"
    out_file = open(out_console_file_path, "w")
    result = subprocess.run(command, text=True, stdout=out_file)
    out_file.close()

    # Check the result
    if result.returncode == 0:
        print("Command executed successfully")
        print("saving the console output!")
        passed_test = 0
        num_tests = 0
        print("============================= Regression Testing =============================")
        # Compare console outputs
        num_tests += 1
        reflog_path = f"{home_env_var}/tests/regressions/reflog/reflog_console.txt"
        out_file_path = out_console_file_path
        test_name = "Console"
        console_test_result = compare_two_files(reflog_path, out_file_path, test_name=test_name,
                                                diff_output_path=config.report_dir)
        passed_test += 1 if console_test_result else 0
        print(f"{test_name} output test: ", "Passed" if console_test_result else "Failed")
        print(f"============================= {passed_test}/{num_tests} regression tests passed ====================")
    else:
        print("Command failed with return code:", result.returncode)
        print("Error:")
        print("Please check tests/regressions/test_output/console_output.txt")
        print(result.stdout)
        print(result.stderr)


if __name__ == "__main__":
    run_regression()
