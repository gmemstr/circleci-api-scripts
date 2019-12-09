# Main testing script that calls all others.
# Sort of a redementary testing framework.
import inspect
import glob
from importlib import import_module

exit = 0

# Get test files, prefixed with `test-`.
def get_tests():
    files = [f for f in glob.glob("tests/test-*.py")]
    processed_files = []

    for name in files:
        f = name.replace(".py", "").replace("tests/", "")
        processed_files.append(f)

    return processed_files


# Dynamically import and run the tests.
def run_tests():
    tests = get_tests()
    for test in tests:
        mod = import_module("tests." + test)
        functions = dir(mod)
        for f in functions:
            if "test_" in f:
                function = getattr(mod, f)
                function()
    global exit
    return exit


def success(msg=""):
    print(inspect.stack()[1][3], "passed", msg)


def fail(msg=""):
    print(inspect.stack()[1][3], "failed", msg)
    global exit
    exit = 1
