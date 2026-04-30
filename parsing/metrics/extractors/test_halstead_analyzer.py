from parsing.metrics.extractors.halstead_analyzer import HalsteadAnalyzer

code = """
public int sum(int a, int b) {
    return a + b;
}
"""

print(HalsteadAnalyzer.analyze(code))