The CMake test target executes all test cases in this directory. During development it can be
handy to be able to execute a specific test case.

```bash
# Replace my_test.py with the name of the module containing the test case you want to execute
PYTHONPATH=../package:$PYTHONPATH python -m unittest my_test.py
```

See this page for more information, for example about executing a single test method:
https://docs.python.org/3/library/unittest.html#command-line-interface
