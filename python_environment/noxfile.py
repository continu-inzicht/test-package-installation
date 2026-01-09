"""
This repository uses [Nox](https://nox.thea.codes/en/stable/) to test development tasks in isolated virtual
environments.
"""

import nox
import os

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = False
nox.options.default_venv_backend = "uv"
nox.options.sessions = ["init", "test"]

TBCI_MAIN_REPO_PATH_TESTS = os.getenv(
    "TBCI_MAIN_REPO_PATH_TESTS", "../../toolbox-continu-inzicht/tests"
)
SUBSET_PATHS = os.getenv("SUBSET_PATHS", "")


@nox.session
def init(session):
    """Initialize the python_environment by installing dependencies."""
    print(
        f"Using TBCI_MAIN_REPO_PATH_TESTS: {TBCI_MAIN_REPO_PATH_TESTS} from .env file"
    )
    print(f"TBCI_MAIN_REPO_PATH_TESTS: {TBCI_MAIN_REPO_PATH_TESTS}")
    session.run("python", "../copy_tests.py", f"{TBCI_MAIN_REPO_PATH_TESTS}")


@nox.session(python="3.11")
# @nox.session(python=["3.11", "3.12", "3.13"])
def test(session):
    session.install(".[test]")
    options = session.posargs
    session.run("python", "-m", "pytest", f"tests/src{SUBSET_PATHS}", "-v", *options)
