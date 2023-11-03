Develop
=======

Code
----

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   API <modules>

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Development environment
-----------------------

.. code-block:: bash

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
   pip install build cmake dash docopt furo jupyterlab ninja pandas plotly pyside6 sphinx

   pathway_generator.py browser
   pathway_generator.py window
   jupyter-lab --notebook-dir=source/notebook/

The project contains code for generating targets, like documentation and the installation
package. Create a new directory for storing these. It is best to create this directory outside
of the source directory. CMake is used to generate build scripts that will do the actual work. We
use the Ninja build tool here, but you can use any build tool supported by CMake.

.. code-block:: bash

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


Create and test a package
-------------------------
Creating a package and inspecting its contents can be done as follows:

.. code-block:: bash

   ninja
   ninja package
   tar -tf dist/adaptation_pathways-1.2.3.tar.gz
   unzip -l dist/adaptation_pathways-1.2.3-py3-none-any.whl

Creating a package (``ninja package``) results in a Wheel file in the ``dist`` directory in
the project's output directory. The next commands can be used to test the package.

.. code-block:: bash

   python3 -m venv ap_test
   source ap_test/bin/activate
   pip install --upgrade pip
   pip install -f dist adaptation_pathways
   adaptation_pathways --help

After testing the package, new versions of the package can be installed like this:

.. code-block:: bash

   pip uninstall --yes adaptation_pathways
   pip install --upgrade -f dist adaptation_pathways


Release a package
-----------------

Create zip with Python Wheel package and the documentation:

.. code-block:: bash

   ninja release

Output is stored in ``adaptation_pathways-1.2.3.zip``.


Create and push a tag.

.. code-block:: bash

   git tag -a v1.2.3 -m"Release that solves all problems"
   git push origin v1.2.3


Background information
----------------------

* Build a package

    * `Python Packaging User Guide <https://packaging.python.org/en/latest/>`_
    * `build packaging frontend <https://pypa-build.readthedocs.io/en/stable/>`_
    * `Hatch packaging backend <https://hatch.pypa.io/latest/>`_
    * `pip package installer <https://pip.pypa.io/en/stable/>`_
