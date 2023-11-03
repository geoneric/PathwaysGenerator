Develop
=======

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   API <modules>


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
   ninja package  # TODO Does not work yet


.. code-block:: bash

   # As a regular user (clean environment). To try out new version of a package. First see the
   # commands mentioned above.
   pip uninstall --yes adaptation_pathways && pip install --upgrade -f dist adaptation_pathways

   # Rebuild the package and check its contents
   ninja && ninja package && tar -tf dist/adaptation_pathways-0.0.1.tar.gz && unzip -l dist/adaptation_pathways-0.0.1-py3-none-any.whl

   # Iterate untill good
   # ...


Build a package
---------------

* `Python Packaging User Guide <https://packaging.python.org/en/latest/>`_
* `build packaging frontend <https://pypa-build.readthedocs.io/en/stable/>`_
* `Hatch packaging backend <https://hatch.pypa.io/latest/>`_
* `pip package installer <https://pip.pypa.io/en/stable/>`_


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
