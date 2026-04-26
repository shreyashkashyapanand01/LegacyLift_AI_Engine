import difflib
import logging

logger = logging.getLogger(__name__)


class DiffGenerator:

    @staticmethod
    def generate(original: str, refactored: str):
        try:
            original_lines = original.splitlines()
            refactored_lines = refactored.splitlines()

            diff = list(difflib.ndiff(original_lines, refactored_lines))

            added = []
            removed = []
            modified = []

            temp_old = None

            for line in diff:
                tag = line[:2]
                content = line[2:]

                # ---------------------------
                # ➕ ADDED
                # ---------------------------
                if tag == "+ ":
                    if temp_old:
                        modified.append({
                            "from": temp_old.strip(),
                            "to": content.strip()
                        })
                        temp_old = None
                    else:
                        if DiffGenerator._is_meaningful(content):
                            added.append(content.strip())

                # ---------------------------
                # ➖ REMOVED
                # ---------------------------
                elif tag == "- ":
                    if DiffGenerator._is_meaningful(content):
                        temp_old = content
                    else:
                        temp_old = None

                # ---------------------------
                # RESET
                # ---------------------------
                else:
                    temp_old = None

            return {
                "added": added,
                "removed": removed,
                "modified": modified
            }

        except Exception:
            logger.exception("Diff generation failed")
            return {"added": [], "removed": [], "modified": []}

    # ---------------------------
    # 🔍 FILTER NOISE
    # ---------------------------
    @staticmethod
    def _is_meaningful(line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        if line in {"{", "}", ";"}:
            return False

        return True