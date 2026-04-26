from parsing.execution_engine.runner.java_runner import JavaRunner
from parsing.execution_engine.test_handler.test_injector import TestInjector

code = """
public int multiply(int a, int b) {
    return a * b;
}
"""

tests = {
    "unit_tests": [
        "multiply(2, 3) returns 6"
    ],
    "edge_cases": [
        "multiply(Integer.MAX_VALUE, 2) throws ArithmeticException"
    ]
}

parsed = TestInjector.parse_tests(tests)

runner = JavaRunner()
results = runner.run(code, parsed)

for r in results:
    print(r)