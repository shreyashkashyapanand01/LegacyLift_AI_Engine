from parsing.rag.refactor_engine.validation.syntax_validator import SyntaxValidator

code = """public int sum(int a, int b) {
    return a + b
}"""

result = SyntaxValidator.validate(code, "java")

print(result)