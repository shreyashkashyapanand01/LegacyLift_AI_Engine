import logging

from parsing.execution_engine.sandbox.temp_workspace import TempWorkspace
from parsing.execution_engine.sandbox.docker_manager import DockerManager

logger = logging.getLogger(__name__)


class JavaRunner:

    def run(self, code: str, test_cases: list):
        results = []

        workspace = TempWorkspace()
        docker = DockerManager()

        try:
            java_file = workspace.create_file(
                "Runner.java",
                self._build_java_code(code, test_cases)
            )

            # ---------------------------
            # 🐳 RUN INSIDE DOCKER
            # ---------------------------
            stdout, stderr = docker.run_java(java_file)
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
            logger.exception("Java execution failed")
            return [{"status": "ERROR", "error": str(e)}]

        finally:
            workspace.cleanup()

    # ---------------------------
    # 🧠 BUILD JAVA FILE
    # ---------------------------
    def _build_java_code(self, user_code, test_cases):

        method_code = user_code.strip()
        main_body = ""

        for test in test_cases:
            inputs = ", ".join(map(str, test["inputs"]))

            if test["type"] == "return":
                main_body += f"""
        try {{
            System.out.println(new Runner().{test['function']}({inputs}));
        }} catch (Exception e) {{
            System.out.println("EXCEPTION:" + e.getClass().getSimpleName());
        }}
"""

            elif test["type"] == "exception":
                main_body += f"""
        try {{
            new Runner().{test['function']}({inputs});
            System.out.println("NO_EXCEPTION");
        }} catch (Exception e) {{
            System.out.println("EXCEPTION:" + e.getClass().getSimpleName());
        }}
"""

        return f"""
public class Runner {{

    public static void main(String[] args) {{
        {main_body}
    }}

    {method_code}
}}
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