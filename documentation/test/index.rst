Test
====

The software can be tested by performing these steps in turn:

#. Create and activate a new virtual environment
#. Install all required Python packages
#. Test the software
#. Remove the virtual environment

This procedure will leave no traces on your computer. If you intent to test the software regularly,
you can keep the virtual environment as is, and install the updated version of the software later.

.. code-block:: bash

   cd ... # prefix of some directory for storing virtual environment
   python3 -m venv ap_test
   source ap_test/bin/activate
   pip3 install --upgrade pip

   cd ... # prefix of dist directory containing package(s)
   pip3 install -f dist adaptation_pathways

   # Use an installed script
   pathways_generator --help

   # Use the package
   python3 -c "import adaptation_pathways as ap; print(ap.__version__)"

   # To clean-up afterwards, just remove the ap_test directory containing the virtual environment
   # ...

Installing an updated version of the software can be done using this command:

.. code-block:: bash

   pip3 install upgrade -f dist adaptation_pathways
