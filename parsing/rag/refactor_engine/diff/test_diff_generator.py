from parsing.rag.refactor_engine.diff.diff_generator import DiffGenerator

original = """public int sum(int a, int b) {
    return a+b;
}"""

refactored = """public int sum(int a, int b) {
    return a + b;
}"""

diff = DiffGenerator.generate(original, refactored)

print(diff)