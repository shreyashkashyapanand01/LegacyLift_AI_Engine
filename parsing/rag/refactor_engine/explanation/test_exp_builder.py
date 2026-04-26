from parsing.rag.refactor_engine.diff.diff_generator import DiffGenerator
from parsing.rag.refactor_engine.explanation.explanation_builder import ExplanationBuilder

original = """public int sum(int a, int b) {
    return a+b;
}"""

refactored = """public int sum(int a, int b) {
    return a + b;
}"""

diff = DiffGenerator.generate(original, refactored)
explanations = ExplanationBuilder.build(diff)

print(explanations)