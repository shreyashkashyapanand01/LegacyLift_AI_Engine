import logging
import traceback

logger = logging.getLogger(__name__)


class PythonRunner:

    # ---------------------------
    # 🚀 MAIN RUNNER
    # ---------------------------
    def run(self, code: str, test_cases: list):
        results = []

        try:
            # ---------------------------
            # 🔹 Create isolated namespace
            # ---------------------------
            exec_globals = {}
            exec(code, exec_globals)

            for test in test_cases:
                result = self._run_single_test(exec_globals, test)
                results.append(result)

            return results

        except Exception:
            logger.exception("Python execution failed")

            return [{
                "status": "ERROR",
                "error": traceback.format_exc()
            }]

    # ---------------------------
    # 🔍 SINGLE TEST EXECUTION
    # ---------------------------
    def _run_single_test(self, scope: dict, test: dict):
        try:
            func_name = test["function"]
            func = scope.get(func_name)

            if not func:
                return {
                    "status": "FAIL",
                    "error": f"Function {func_name} not found"
                }

            inputs = test["inputs"]

            # ---------------------------
            # 🧪 RETURN TEST
            # ---------------------------
            if test["type"] == "return":
                expected = test["expected"]

                output = func(*inputs)

                if output == expected:
                    return {
                        "status": "PASS",
                        "output": output
                    }
                else:
                    return {
                        "status": "FAIL",
                        "expected": expected,
                        "actual": output
                    }

            # ---------------------------
            # ⚠️ EXCEPTION TEST
            # ---------------------------
            elif test["type"] == "exception":
                expected_exception = test["expected_exception"]

                try:
                    func(*inputs)

                    return {
                        "status": "FAIL",
                        "error": "Exception not raised"
                    }

                except Exception as e:
                    if expected_exception in type(e).__name__:
                        return {
                            "status": "PASS",
                            "exception": type(e).__name__
                        }
                    else:
                        return {
                            "status": "FAIL",
                            "expected_exception": expected_exception,
                            "actual_exception": type(e).__name__
                        }

        except Exception:
            return {
                "status": "ERROR",
                "error": traceback.format_exc()
            }