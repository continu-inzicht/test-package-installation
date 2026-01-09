import os
import sys
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import toml
from datetime import datetime


def read_main_repo_toml(TBCI_MAIN_REPO_PATH):
    toml_path = Path(TBCI_MAIN_REPO_PATH) / "src" / "pyproject.toml"
    data: dict = toml.load(toml_path)
    categories = data["project"]["optional-dependencies"]
    return list(categories.keys())


def tweak_toml(TBCI_MAIN_REPO_PATH, version):
    toml_path = Path(__file__).parent / "python_environment" / "pyproject.toml"

    # with toml_path.open("rb") as f:
    data = toml.load(str(toml_path))

    dependencies = data["project"]["dependencies"]

    # Find and replace the toolbox-continu-inzicht dependency
    for i, dep in enumerate(dependencies):
        if dep.startswith("toolbox-continu-inzicht"):
            dependencies[i] = (
                f"toolbox-continu-inzicht[{version}] @ file:///{TBCI_MAIN_REPO_PATH}/src"
            )
            break

    with toml_path.open("w") as f:
        toml.dump(data, f)


def remove_venvs():
    venv_path = Path(__file__).parent / "python_environment" / ".nox"
    if venv_path.exists() and venv_path.is_dir():
        shutil.rmtree(venv_path)


def write_to_log(result, subset_paths_tests, version, log_file):
    with log_file.open("a") as f:
        f.write(f"\n{'=' * 80}\n")
        f.write(f"Version: {version}, test path: {subset_paths_tests}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 80}\n")
        f.write(result.stdout)
        f.write(result.stderr)


def run_tests(args):
    load_dotenv(".env")
    log_name = os.getenv("TEST_LOG_NAME", "test_results.log")
    log_file = Path(__file__).parent / log_name
    # when logging no verspose is shown in terminal, easier to debug test but more difficult to debug uv/nox
    # also set from the commandline args
    log = True

    # read all the possible installation categories from the main repo pyproject.toml
    TBCI_MAIN_REPO_PATH = os.getenv(
        "TBCI_MAIN_REPO_PATH", "../../toolbox-continu-inzicht"
    )
    PYTHON_VERSIONS = os.getenv(
        "PYTHON_VERSIONS", "3.11"
    )  # For the tests runner this is set in the test.yml
    os.environ["PYTHON_VERSIONS"] = PYTHON_VERSIONS  # pass it to noxfile.py

    categories = read_main_repo_toml(TBCI_MAIN_REPO_PATH)
    # in case of arguments, only run for that category
    if len(args) > 1 and args[1] in categories:
        categories = [args[1]]
    for arg in args[1:]:
        if arg.startswith("log="):
            log_value = arg.split("=")[1]
            log = log_value.lower() in ("y", "yes", "true", "True", "1")

    for instalation_version in categories:
        remove_venvs()
        print(f"Running tests for version: {instalation_version}")
        tweak_toml(TBCI_MAIN_REPO_PATH, instalation_version)
        # passed onto the noxfile.py env
        os.environ["TBCI_MAIN_REPO_PATH_TESTS"] = f"{TBCI_MAIN_REPO_PATH}/tests"
        # Most versions/modules have their respective test folders, others don't
        match instalation_version:
            case "all":
                subset_paths_tests = ""
            case "io":
                subset_paths_tests = "/base"
            case _:
                subset_paths_tests = f"/{instalation_version}"

        os.environ["SUBSET_PATHS"] = subset_paths_tests
        if log:  # easier to fix issues as teh verbose is quite long
            result = subprocess.run(
                ["uvx", "nox", "-s"],
                cwd="python_environment",
                capture_output=True,
                text=True,
            )
            write_to_log(result, subset_paths_tests, instalation_version, log_file)
        else:  # easier to see whats going on with uv/nox
            subprocess.run(
                ["uvx", "nox", "-s"],
                cwd="python_environment",
            )
    remove_venvs()


if __name__ == "__main__":
    run_tests(sys.argv)
