from parsing.execution_engine.comparator.output_comparator import OutputComparator

original = [
    {"status": "PASS", "output": 6},
    {"status": "FAIL", "error": "NO_EXCEPTION"}
]

refactored = [
    {"status": "PASS", "output": 6},
    {"status": "PASS", "exception": "ArithmeticException"}
]

result = OutputComparator.compare(original, refactored)

print(result)