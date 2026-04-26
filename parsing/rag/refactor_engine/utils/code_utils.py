import re
import logging

from parsing.rag.refactor_engine.formatter.python_formatter import PythonFormatter
from parsing.rag.refactor_engine.formatter.java_formatter import JavaFormatter

logger = logging.getLogger(__name__)


class CodeUtils:

    # ---------------------------
    # 🔍 LANGUAGE DETECTION
    # ---------------------------
    @staticmethod
    def detect_language(code: str) -> str:
        try:
            if not code:
                return "unknown"

            code_lower = code.lower()

            # 🔹 JAVA DETECTION
            if (
                "public class" in code_lower or
                "public static void main" in code_lower or
                re.search(r"\b(int|void|double|string)\s+\w+\s*\(", code_lower)
            ):
                return "java"

            # 🔹 PYTHON DETECTION
            if (
                "def " in code_lower or
                "import " in code_lower or
                "print(" in code_lower
            ):
                return "python"

            return "unknown"

        except Exception:
            logger.warning("Language detection failed")
            return "unknown"

    # ---------------------------
    # 🎨 FORMATTER ROUTER
    # ---------------------------
    @staticmethod
    def format_code(code: str, language: str):
        """
        Returns:
            formatted_code (str)
            formatting_applied (bool)
        """
        try:
            if not code:
                return "", False

            if language == "python":
                return PythonFormatter.format(code), True

            elif language == "java":
                return JavaFormatter.format(code), True

            # fallback
            return code, False

        except Exception:
            logger.warning("Formatting failed")
            return code, False