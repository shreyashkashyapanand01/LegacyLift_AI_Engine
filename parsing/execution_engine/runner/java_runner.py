import os
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)


class JavaRunner:

    def run(self, code: str, test_cases: list):
        results = []

        try:
            with tempfile.TemporaryDirectory() as temp_dir:

                java_file = os.path.join(temp_dir, "Runner.java")

                # ---------------------------
                # 🧠 BUILD FULL JAVA CODE
                # ---------------------------
                full_code = self._build_java_code(code, test_cases)

                with open(java_file, "w") as f:
                    f.write(full_code)

                # ---------------------------
                # ⚙️ COMPILE
                # ---------------------------
                compile_proc = subprocess.run(
                    ["javac", java_file],
                    capture_output=True,
                    text=True
                )

                if compile_proc.returncode != 0:
                    return [{
                        "status": "ERROR",
                        "error": compile_proc.stderr
                    }]

                # ---------------------------
                # ▶ RUN
                # ---------------------------
                run_proc = subprocess.run(
                    ["java", "-cp", temp_dir, "Runner"],
                    capture_output=True,
                    text=True
                )

                output_lines = run_proc.stdout.strip().split("\n")

                # ---------------------------
                # 🧪 MATCH OUTPUTS
                # ---------------------------
                for i, test in enumerate(test_cases):
                    results.append(self._evaluate_output(test, output_lines, i))

                return results

        except Exception as e:
            logger.exception("Java execution failed")

            return [{
                "status": "ERROR",
                "error": str(e)
            }]

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

        # ---------------------------
        # RETURN TEST
        # ---------------------------
        if test["type"] == "return":
            expected = str(test["expected"])

            if output == expected:
                return {"status": "PASS", "output": output}
            else:
                return {
                    "status": "FAIL",
                    "expected": expected,
                    "actual": output
                }

        # ---------------------------
        # EXCEPTION TEST
        # ---------------------------
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