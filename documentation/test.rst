Test
====

.. code-block:: bash

   # Create and activate a new virtual environment (here called ap_test). This will create a
   # directory called ap_test.
   cd ... # prefix of directory for storing virtual environment
   python3 -m venv ap_test
   source ap_test/bin/activate
   pip install --upgrade pip

   cd ... # prefix of dist directory containing package(s)
   pip install -f dist adaptation_pathways

   # This should work now
   adaptation_pathways --help

   # To clean-up afterwards, just remove the ap_test directory containing the virtual environment
   # ...
