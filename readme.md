# Extra testing

Check to see if splitting pypi package it works.

## route 1: fully automatic with UV

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Ensure `TBCI_MAIN_REPO_PATH="..."` is set to your repo of the main TBCI instance.

### Running the script will

- initialise the tests by copying them over from the main repo to here.
- run tests on versions of python specified (>=3.11)
- loops over the different 'instalation version' of the toolbox
    > so aside from toolbox-continu-inzicht[all], it also checks all the possible install options [loads]/[sections]
    > you can specify arguments to run just one with `run_tests_uv.py inspections`
- default logging is written to test_results.log, you can enable/disable with with `run_tests_uv.py inspections log=true`/`log=false`
- many warnings are expected, the toolbox is set up in such a way to throw warnings when missing a package. In production these can be silenced.
- total runtime per python version is 6min, for 3 versions (3.11, 3.12, 3.13) python verions this takes roughly 15 - 30min.

#### using your own environment

Run `python run_tests_uv.py` to start the process of testing.
This will call uv itself, you can have a simple python dev environment locally to run this, uv will create venv to do testing in.
You only need `python-dotenv` & `toml` to load those the .env file.  

#### using uv

You can also use provided uv environment in highest directory for this.
Not to be confused with the testing environment in `\python_environment`.
Run `uv sync --locked` for this, a new uv environment will be made.
Run`uv run run_tests.py`, any arguments can follow: `uv run run_tests.py loads log=false`

## route 2: manually via conda

(old was of doing it: more labour intesive)

Replace `C:\Data\Python\TBCI\toolbox-continu-inzicht` with your own path.

```bash
# setup env
conda env create -n tbcit1
conda activate tbcit1
conda install pytest benchmark -y
# copy tests
python copy_tests.py "C:\Data\Python\TBCI\toolbox-continu-inzicht\tests"

# install & check - run in conda termninal
pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[loads]
python run_tests.py loads

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[inspections]
python run_tests.py inspections

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[sections]
python run_tests.py sections

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[flood_scenarios]
python run_tests.py flood_scenarios

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[fragility_curves]
python run_tests.py fragility_curves

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[io]
python run_tests.py io
```

```bash
conda env create -n tbcit2 -f "C:\Data\Python\TBCI\toolbox-continu-inzicht\src\requirements.yaml"
conda activate tbcit2
conda install pytest benchmark -y

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[all]
python run_tests.py all
```
