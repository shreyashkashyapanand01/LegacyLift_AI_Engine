from parsing.metrics.pipeline.metrics_pipeline import MetricsPipeline

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

print(MetricsPipeline.run(original_code, refactored_code, "java"))