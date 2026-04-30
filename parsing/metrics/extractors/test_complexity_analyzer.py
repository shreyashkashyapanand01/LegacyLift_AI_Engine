from parsing.metrics.extractors.java.complexity_analyzer import JavaComplexity
from parsing.metrics.extractors.python.complexity_analyzer import PythonComplexity

java_code = """
public int sum(int a, int b) {
    if (a > 0 && b > 0) {
        return a + b;
    }
    return 0;
}
"""

python_code = """
def sum(a, b):
    if a > 0 and b > 0:
        return a + b
    return 0
"""

print("JAVA:", JavaComplexity.analyze(java_code))
print("PYTHON:", PythonComplexity.analyze(python_code))