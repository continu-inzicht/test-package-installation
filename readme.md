# Extra testing

Sanitiy check to see if splitting pypi package it works.

## route 1: via seperate streams

Replace `C:\Data\Python\TBCI\toolbox-continu-inzicht` with your own path.

```bash
# setup env
conda env create -n tbcit1
conda activate tbcit1
conda install pytest, benchmark
# copy tests
python copy_tests.py "C:\Data\Python\TBCI\toolbox-continu-inzicht\tests"

# install & check - run in conda termninal
pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[loads]
python run_tests.py loads

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[sections]
python run_tests.py sections

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[flood_scenarios]
python run_tests.py flood_scenarios # geeft wat fouten op paden maar werkt wel

pip install "C:\Data\Python\TBCI\toolbox-continu-inzicht\src"[fragility_curves]
python run_tests.py fragility_curves # geeft wat fouten op paden maar werkt wel


```

```bash
conda env create -n tbcit2 -f "C:\Data\Python\TBCI\toolbox-continu-inzicht\src\requirements.yaml"
conda activate tbcit2

```
