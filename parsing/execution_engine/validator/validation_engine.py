import logging

from parsing.execution_engine.test_handler.test_injector import TestInjector
from parsing.execution_engine.runner.python_runner import PythonRunner
from parsing.execution_engine.runner.java_runner import JavaRunner
from parsing.execution_engine.comparator.output_comparator import OutputComparator

logger = logging.getLogger(__name__)


class ValidationEngine:

    def __init__(self):
        self.python_runner = PythonRunner()
        self.java_runner = JavaRunner()

    # ---------------------------
    # 🚀 MAIN VALIDATION
    # ---------------------------
    def validate(
        self,
        original_code: str,
        refactored_code: str,
        tests: dict,
        language: str
    ):
        try:
            # ---------------------------
            # 🧪 PARSE TESTS
            # ---------------------------
            parsed_tests = TestInjector.parse_tests(tests)

            if not parsed_tests:
                return self._error("No valid test cases")

            # ---------------------------
            # 🏃 SELECT RUNNER
            # ---------------------------
            runner = self._get_runner(language)

            if not runner:
                return self._error(f"Unsupported language: {language}")

            # ---------------------------
            # ▶ RUN ORIGINAL
            # ---------------------------
            original_results = runner.run(original_code, parsed_tests)

            # ---------------------------
            # ▶ RUN REFACTORED
            # ---------------------------
            refactored_results = runner.run(refactored_code, parsed_tests)

            # ---------------------------
            # ⚖️ COMPARE
            # ---------------------------
            comparison = OutputComparator.compare(
                original_results,
                refactored_results
            )

            # ---------------------------
            # 📤 FINAL RESPONSE
            # ---------------------------
            return {
                "status": comparison["status"],
                "confidence": comparison["confidence"],
                "summary": comparison["summary"],
                "failed_cases": comparison["failed_cases"],
                "original_results": original_results,
                "refactored_results": refactored_results
            }

        except Exception:
            logger.exception("Validation engine failed")

            return self._error("Validation execution failed")

    # ---------------------------
    # 🔍 RUNNER SELECTOR
    # ---------------------------
    def _get_runner(self, language: str):
        language = (language or "").lower()

        if language == "python":
            return self.python_runner
        elif language == "java":
            return self.java_runner

        return None

    # ---------------------------
    # ❌ ERROR HANDLER
    # ---------------------------
    def _error(self, message: str):
        return {
            "status": "ERROR",
            "confidence": 0,
            "summary": message,
            "failed_cases": [],
            "original_results": [],
            "refactored_results": []
        }