from parsing.metrics.extractors.base_analyzer import BaseAnalyzer


class PythonComplexity:

    @staticmethod
    def analyze(code: str):
        code = BaseAnalyzer.normalize_code(code)

        keywords = [
            "if", "elif", "for", "while", "except"
        ]

        logical_ops = ["and", "or"]

        decision_points = 0

        # keyword-based
        for kw in keywords:
            decision_points += BaseAnalyzer.count_decision_points(code, [kw])

        # logical operators
        for op in logical_ops:
            decision_points += code.count(op)

        complexity = 1 + decision_points

        return {
            "complexity": complexity
        }