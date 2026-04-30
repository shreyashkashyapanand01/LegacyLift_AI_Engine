from parsing.metrics.extractors.base_analyzer import BaseAnalyzer

code = """
public int sum(int a, int b) {
    return a + b;
}
"""

print(BaseAnalyzer.get_lines(code))
print(BaseAnalyzer.tokenize(code))