Unit tests are stored in a directory that has a unique name (``ap_test``). This is to prevent
name clashes between other modules, from the Python standard library, from other packages,
or from our own package.

The CMake test target executes all test cases in this directory. During development it can be
handy to be able to execute a specific test case.

```bash
# Replace my_test.py with the name of the module containing the test case you want to execute
PYTHONPATH=../package:$PYTHONPATH python -m unittest ap_test/my_test.py
```

Example for executing a specific test method:

```bash
python -m unittest ap_test.io.sqlite_test.SQLiteTest.test_action_combination_02_pathway
```

See this page for more information:
https://docs.python.org/3/library/unittest.html#command-line-interface
