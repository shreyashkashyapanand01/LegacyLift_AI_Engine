from parsing.metrics.feature_builder.feature_engineer import FeatureEngineer

code = """
public int sum(int a, int b) {
    return a + b;
}
"""

print(FeatureEngineer.build(code, "java"))