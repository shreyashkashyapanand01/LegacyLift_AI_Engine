from parsing.metrics.extractors.java.loc_counter import JavaLOC
from parsing.metrics.extractors.python.loc_counter import PythonLOC

java_code = """
public int sum(int a, int b) {
    // add numbers
    return a + b;
}
"""

python_code = """
def sum(a, b):
    # add numbers
    return a + b
"""

print("JAVA:", JavaLOC.analyze(java_code))
print("PYTHON:", PythonLOC.analyze(python_code))