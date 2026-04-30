from parsing.metrics.extractors.python.loc_counter import PythonLOC
from parsing.metrics.extractors.java.loc_counter import JavaLOC

from parsing.metrics.extractors.python.complexity_analyzer import PythonComplexity
from parsing.metrics.extractors.java.complexity_analyzer import JavaComplexity

from parsing.metrics.extractors.halstead_analyzer import HalsteadAnalyzer
from parsing.metrics.extractors.maintainability import MaintainabilityAnalyzer


class FeatureEngineer:

    @staticmethod
    def build(code: str, language: str):
        """
        Build structured feature set from code
        """

        # ---------------------------
        # LOC
        # ---------------------------
        if language == "python":
            loc_data = PythonLOC.analyze(code)
            complexity_data = PythonComplexity.analyze(code)

        elif language == "java":
            loc_data = JavaLOC.analyze(code)
            complexity_data = JavaComplexity.analyze(code)

        else:
            return {}

        # ---------------------------
        # HALSTEAD
        # ---------------------------
        halstead = HalsteadAnalyzer.analyze(code)

        # ---------------------------
        # MAINTAINABILITY
        # ---------------------------
        maintainability = MaintainabilityAnalyzer.analyze(
            volume=halstead["volume"],
            complexity=complexity_data["complexity"],
            loc=loc_data["effective_lines"]
        )

        # ---------------------------
        # FINAL FEATURE SET
        # ---------------------------
        return {
            "complexity": complexity_data["complexity"],
            "loc": loc_data["effective_lines"],
            "comment_lines": loc_data["comment_lines"],
            "maintainability": maintainability["maintainability_index"],
            "halstead": {
                "volume": halstead["volume"],
                "difficulty": halstead["difficulty"],
                "effort": halstead["effort"]
            }
        }