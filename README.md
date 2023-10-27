# Adaptation pathways

https://publicwiki.deltares.nl/display/AP/Adaptation+Pathways


```bash
# Create virtual environment that will contain all packages we need:
# https://docs.python.org/3/library/venv.html
python3 -m venv env
source env/bin/activate
pip install --upgrade pip

# Install handy tools that will keep our code in good shape:
# https://pre-commit.com
pip install pre-commit
pre-commit install
# Optional, commit .pre-commit-config.yaml if any hooks got updated
pre-commit autoupdate

# Use a local updated version of pylint instead of the older version possibly installed on
# the system and instead of the normal pylint pre-commit hook. pre-commit hooks run in their own
# virtual environment that doesn't know about our package.
pip install pylint

# Install software our code depends on:
pip install cmake dash docopt jupyterlab ninja pandas plotly pyside6 sphinx

pathway_generator.py browser
pathway_generator.py window
jupyter-lab --notebook-dir=source/notebook/
```

The project contains code for generating targets, like documentation and the installation
package. Create a new directory for storing these. It is best to create this directory outside
of the source directory. CMake is used to generate build scripts that will do the actual work. We
use the Ninja build tool here, but you can use any build tool supported by CMake.

```bash
# Assuming we are in the adaptation_pathways source directory...

mkdir ../build
cd ../build
cmake -S ../adaptation_pathways -G Ninja

# Execute the tests
ninja test

# Generate the documentation
ninja documentation

# Create the package
ninja package
```
