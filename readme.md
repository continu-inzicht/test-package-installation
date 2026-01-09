# Extra testing

Sanitiy check to see if splitting pypi package it works.

## route 1: manually via conda

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
# missing scipy?

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[inspections]
python run_tests.py inspections

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[sections]
python run_tests.py sections

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[flood_scenarios]
python run_tests.py flood_scenarios # geeft wat fouten op paden maar werkt wel

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

## route 2: semi-automatic with UV

Replace `C:\Data\Python\TBCI\toolbox-continu-inzicht` with your own path.

```bash
cd python_environment
uvx python ..\copy_tests.py "C:\Data\Python\TBCI\toolbox-continu-inzicht\tests"
uvx nox -s
```

This proceeds to run the tests, but we need to loop over the toolbox versions we make availible.

## route 3: fully automatic with UV

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Ensure `TBCI_MAIN_REPO_PATH="..."` is set to your repo of the main TBCI instance.

Run `python run_tests_uv.py` to start the process of testing. This will call uv itself, you can have a simple python dev environment locally to run this, uv will create venv to do testing in. You only need `python-dotenv` & `toml` to load those the .env file.

This will:

- initialise the tests by copying them over from the main repo to here.
- run tests on versions of python specified (>=3.11)
- loops over the different 'instalation version' of the toolbox
    > so aside from toolbox-continu-inzicht[all], it also checks all the possible install options [loads]/[sections]
    > you can specify to run just one with `python run_tests_uv.py inspections`
- default logging is written to test_results.log, you can enable/disable with with `python run_tests_uv.py inspections log=true`/`log=false`
- many warnings are expected, the toolbox is set up in such a way to throw warnings when missing a package. In production these can be silenced.
- total runtime per instaltion is 2min, for 6 versions of the package and 3 (3.11,3.12,3.13) python verions this takes roughly half an hour.
