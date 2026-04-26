from parsing.execution_engine.validator.validation_engine import ValidationEngine

original_code = """
public int multiply(int a, int b) {
    return a * b;
}
"""

refactored_code = """
public int multiply(int a, int b) {
    return Math.multiplyExact(a, b);
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

engine = ValidationEngine()

result = engine.validate(
    original_code=original_code,
    refactored_code=refactored_code,
    tests=tests,
    language="java"
)

print(result)