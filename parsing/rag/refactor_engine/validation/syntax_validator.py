import logging
import re

logger = logging.getLogger(__name__)


class SyntaxValidator:

    @staticmethod
    def validate(code: str, language: str):
        try:
            if not code:
                return {
                    "is_valid": False,
                    "errors": ["Empty code"]
                }

            if language == "java":
                return SyntaxValidator._validate_java(code)

            elif language == "python":
                return SyntaxValidator._validate_python(code)

            return {
                "is_valid": True,
                "errors": []
            }

        except Exception:
            logger.exception("Syntax validation failed")
            return {
                "is_valid": False,
                "errors": ["Validation failed"]
            }

    # ---------------------------
    # ☕ JAVA VALIDATION (BASIC)
    # ---------------------------
    @staticmethod
    def _validate_java(code: str):
        errors = []

        # 🔹 check semicolons
        lines = code.split("\n")
        for i, line in enumerate(lines):
            line = line.strip()

            if (
                line and
                not line.endswith(";") and
                not line.endswith("{") and
                not line.endswith("}") and
                not line.startswith("//")
            ):
                errors.append(f"Line {i+1}: Missing semicolon")

        # 🔹 bracket balance
        if code.count("{") != code.count("}"):
            errors.append("Mismatched braces")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    # ---------------------------
    # 🐍 PYTHON VALIDATION
    # ---------------------------
    @staticmethod
    def _validate_python(code: str):
        errors = []

        try:
            compile(code, "<string>", "exec")
        except Exception as e:
            errors.append(str(e))

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }