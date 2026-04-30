import math
from parsing.metrics.extractors.base_analyzer import BaseAnalyzer


class HalsteadAnalyzer:

    @staticmethod
    def analyze(code: str):
        code = BaseAnalyzer.normalize_code(code)

        tokens = BaseAnalyzer.tokenize(code)

        operators, operands = BaseAnalyzer.get_operators_operands(tokens)

        # ---------------------------
        # COUNTS
        # ---------------------------
        unique_operators = set(operators)
        unique_operands = set(operands)

        n1 = len(unique_operators)
        n2 = len(unique_operands)

        N1 = len(operators)
        N2 = len(operands)

        # ---------------------------
        # SAFE GUARDS
        # ---------------------------
        if n1 == 0 or n2 == 0:
            return {
                "n1": n1,
                "n2": n2,
                "N1": N1,
                "N2": N2,
                "vocabulary": 0,
                "length": 0,
                "volume": 0,
                "difficulty": 0,
                "effort": 0
            }

        vocabulary = n1 + n2
        length = N1 + N2

        # avoid log(0)
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0

        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0

        effort = volume * difficulty

        return {
            "n1": n1,
            "n2": n2,
            "N1": N1,
            "N2": N2,
            "vocabulary": vocabulary,
            "length": length,
            "volume": round(volume, 2),
            "difficulty": round(difficulty, 2),
            "effort": round(effort, 2)
        }