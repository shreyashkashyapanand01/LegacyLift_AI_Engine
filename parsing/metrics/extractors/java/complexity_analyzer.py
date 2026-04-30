from parsing.metrics.extractors.base_analyzer import BaseAnalyzer


class JavaComplexity:

    @staticmethod
    def analyze(code: str):
        code = BaseAnalyzer.normalize_code(code)

        keywords = [
            "if", "for", "while", "case", "catch"
        ]

        decision_points = 0

        # keyword-based
        for kw in keywords:
            decision_points += BaseAnalyzer.count_decision_points(code, [kw])

        # logical operators
        decision_points += code.count("&&")
        decision_points += code.count("||")

        complexity = 1 + decision_points

        return {
            "complexity": complexity
        }