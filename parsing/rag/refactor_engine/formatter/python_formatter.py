import logging
import re

logger = logging.getLogger(__name__)


class PythonFormatter:

    @staticmethod
    def format(code: str) -> str:
        try:
            import autopep8

            code = autopep8.fix_code(code)

            # 🔥 FIX OPERATORS (extra safety)
            code = re.sub(r'(\w)([+\-*/=])(\w)', r'\1 \2 \3', code)

            return code

        except Exception:
            logger.warning("Python formatting failed, returning original")
            return code