from parsing.execution_engine.test_handler.test_injector import TestInjector

tests = {
    "unit_tests": [
        "multiply(2, 3) returns 6"
    ],
    "edge_cases": [
        "multiply(Integer.MAX_VALUE, 2) throws ArithmeticException"
    ]
}

parsed = TestInjector.parse_tests(tests)

for t in parsed:
    print(t)