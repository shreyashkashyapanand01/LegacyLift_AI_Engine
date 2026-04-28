import logging

from parsing.execution_engine.sandbox.temp_workspace import TempWorkspace
from parsing.execution_engine.sandbox.docker_manager import DockerManager

logger = logging.getLogger(__name__)


class PythonRunner:

    def run(self, code: str, test_cases: list):
        results = []

        workspace = TempWorkspace()
        docker = DockerManager()

        try:
            # ---------------------------
            # 🔹 CREATE FILE
            # ---------------------------
            full_code = self._build_python_code(code, test_cases)
            file_path = workspace.create_file("runner.py", full_code)

            # ---------------------------
            # 🐳 RUN INSIDE DOCKER
            # ---------------------------
            stdout, stderr = docker.run_python(file_path)
            print("RUNNING INSIDE DOCKER")

            if stderr:
                return [{"status": "ERROR", "error": stderr.strip()}]

            output_lines = stdout.strip().split("\n") if stdout else []

            # ---------------------------
            # 🧪 MATCH OUTPUTS
            # ---------------------------
            for i, test in enumerate(test_cases):
                results.append(self._evaluate_output(test, output_lines, i))

            return results

        except Exception as e:
            logger.exception("Python execution failed")
            return [{"status": "ERROR", "error": str(e)}]

        finally:
            workspace.cleanup()

    # ---------------------------
    # 🧠 BUILD PYTHON FILE
    # ---------------------------
    def _build_python_code(self, user_code, test_cases):

        main_body = ""

        for test in test_cases:
            inputs = ", ".join(map(str, test["inputs"]))

            if test["type"] == "return":
                main_body += f"""
try:
    print({test['function']}({inputs}))
except Exception as e:
    print("EXCEPTION:" + type(e).__name__)
"""

            elif test["type"] == "exception":
                main_body += f"""
try:
    {test['function']}({inputs})
    print("NO_EXCEPTION")
except Exception as e:
    print("EXCEPTION:" + type(e).__name__)
"""

        return f"""
{user_code}

if __name__ == "__main__":
{main_body}
"""

    # ---------------------------
    # 🔍 OUTPUT EVALUATION
    # ---------------------------
    def _evaluate_output(self, test, outputs, index):

        if index >= len(outputs):
            return {"status": "ERROR", "error": "Missing output"}

        output = outputs[index].strip()

        if test["type"] == "return":
            expected = str(test["expected"])

            if output == expected:
                return {"status": "PASS", "output": output}
            else:
                return {"status": "FAIL", "expected": expected, "actual": output}

        elif test["type"] == "exception":
            expected_exception = test["expected_exception"]

            if f"EXCEPTION:{expected_exception}" == output:
                return {"status": "PASS", "exception": expected_exception}
            else:
                return {
                    "status": "FAIL",
                    "expected_exception": expected_exception,
                    "actual": output
                }