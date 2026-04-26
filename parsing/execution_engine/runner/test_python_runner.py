from parsing.execution_engine.runner.python_runner import PythonRunner
from parsing.execution_engine.test_handler.test_injector import TestInjector

code = """
def multiply(a, b):
    return a * b
"""

tests = {
    "unit_tests": [
        "multiply(2, 3) returns 6"
    ],
    "edge_cases": [
        "multiply(2, 0) returns 0"
    ]
}

parsed_tests = TestInjector.parse_tests(tests)

runner = PythonRunner()
results = runner.run(code, parsed_tests)

for r in results:
    print(r)