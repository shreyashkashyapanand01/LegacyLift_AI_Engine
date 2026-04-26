import logging
import re

logger = logging.getLogger(__name__)


class JavaFormatter:

    @staticmethod
    def format(code: str) -> str:
        try:
            if not code:
                return ""

            # 🔹 Fix operators
            code = re.sub(r'(\w)([+\-*/=])(\w)', r'\1 \2 \3', code)

            # 🔹 Add line breaks
            code = code.replace("{", "{\n")
            code = code.replace("}", "\n}")
            code = code.replace(";", ";\n")

            # 🔹 Clean extra lines
            code = re.sub(r"\n\s*\n+", "\n", code)

            # 🔹 Indentation
            lines = code.split("\n")
            formatted_lines = []

            indent_level = 0

            for line in lines:
                line = line.strip()

                if line.endswith("}"):
                    indent_level -= 1

                formatted_lines.append("    " * max(indent_level, 0) + line)

                if line.endswith("{"):
                    indent_level += 1

            return "\n".join(formatted_lines)

        except Exception:
            logger.warning("Java formatting failed, returning original")
            return code