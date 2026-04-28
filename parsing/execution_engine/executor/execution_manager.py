import logging
from typing import Dict, Any

from parsing.execution_engine.runner.python_runner import PythonRunner
from parsing.execution_engine.runner.java_runner import JavaRunner
from parsing.execution_engine.test_handler.test_injector import TestInjector
from parsing.execution_engine.comparator.output_comparator import OutputComparator
from parsing.execution_engine.validator.validation_engine import ValidationEngine

logger = logging.getLogger(__name__)


class ExecutionManager:

    def __init__(self):
        self.python_runner = PythonRunner()
        self.java_runner = JavaRunner()

    # ---------------------------
    # 🚀 MAIN EXECUTION PIPELINE
    # ---------------------------
    def execute(
        self,
        language: str,
        original_code: str,
        refactored_code: str,
        tests: Dict[str, Any]
    ) -> Dict:

        try:
            logger.info("Starting execution validation pipeline")

            # ---------------------------
            # 🧪 BUILD TEST CASES
            # ---------------------------
            test_cases = TestInjector.parse_tests(tests)

            # ---------------------------
            # 🏃 SELECT RUNNER
            # ---------------------------
            runner = self._get_runner(language)

            if not runner:
                raise ValueError(f"Unsupported language: {language}")

            # ---------------------------
            # ▶ RUN ORIGINAL CODE
            # ---------------------------
            original_results = runner.run(original_code, test_cases)

            # ---------------------------
            # ▶ RUN REFACTORED CODE
            # ---------------------------
            refactored_results = runner.run(refactored_code, test_cases)

            # ---------------------------
            # ⚖️ COMPARE OUTPUTS
            # ---------------------------
            comparison = OutputComparator.compare(
                original_results,
                refactored_results
            )

            # ---------------------------
            # ✅ FINAL VALIDATION
            # ---------------------------
            validation_result = ValidationEngine.evaluate(comparison)

            return {
                "original_results": original_results,
                "refactored_results": refactored_results,
                "comparison": comparison,
                "validation": validation_result
            }

        except Exception:
            logger.exception("Execution pipeline failed")

            return {
                "original_results": [],
                "refactored_results": [],
                "comparison": [],
                "validation": {
                    "status": "FAIL",
                    "confidence": 0.0,
                    "failed_cases": ["Execution failed"]
                }
            }

    # ---------------------------
    # 🔧 RUNNER SELECTOR
    # ---------------------------
    def _get_runner(self, language: str):
        language = language.lower()

        if language == "python":
            return self.python_runner

        if language == "java":
            return self.java_runner

        return None