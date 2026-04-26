import re
import logging

logger = logging.getLogger(__name__)


class CodeCleaner:

    @staticmethod
    def clean(code: str) -> str:
        try:
            if not code:
                return ""

            # ---------------------------
            # 🔹 Remove leading/trailing spaces
            # ---------------------------
            code = code.strip()

            # ---------------------------
            # 🔹 Normalize line endings
            # ---------------------------
            code = code.replace("\r\n", "\n").replace("\r", "\n")

            # ---------------------------
            # 🔹 Remove excessive blank lines
            # ---------------------------
            code = re.sub(r"\n\s*\n+", "\n\n", code)

            # ---------------------------
            # 🔹 Fix indentation (basic normalization)
            # ---------------------------
            lines = code.split("\n")
            cleaned_lines = [line.rstrip() for line in lines]
            code = "\n".join(cleaned_lines)

            # ---------------------------
            # 🔹 Remove trailing semicolon-only lines (noise)
            # ---------------------------
            code = re.sub(r"^\s*;\s*$", "", code, flags=re.MULTILINE)

            # ---------------------------
            # 🔹 Remove weird LLM artifacts
            # ---------------------------
            code = code.replace("```java", "").replace("```", "")

            # ---------------------------
            # 🔹 Final trim
            # ---------------------------
            code = code.strip()

            return code

        except Exception:
            logger.exception("Code cleaning failed")
            return code  # fallback (never break pipeline)