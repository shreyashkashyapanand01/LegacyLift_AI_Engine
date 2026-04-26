import logging

logger = logging.getLogger(__name__)


class ExplanationBuilder:

    @staticmethod
    def build(diff: dict):
        try:
            explanations = []

            # ---------------------------
            # 🔹 MODIFIED
            # ---------------------------
            for change in diff.get("modified", []):
                old = change.get("from", "")
                new = change.get("to", "")

                explanations.append(
                    ExplanationBuilder._analyze_change(old, new)
                )

            # ---------------------------
            # 🔹 ADDED
            # ---------------------------
            for line in diff.get("added", []):
                if ExplanationBuilder._is_noise(line):
                    continue

                explanations.append({
                    "change": ExplanationBuilder._summarize_line(line),
                    "impact": "Adds new functionality or improves robustness",
                    "type": "addition"
                })

            # ---------------------------
            # 🔹 REMOVED
            # ---------------------------
            for line in diff.get("removed", []):
                if ExplanationBuilder._is_noise(line):
                    continue

                explanations.append({
                    "change": f"Removed unnecessary code: {line.strip()}",
                    "impact": "Improves code clarity and maintainability",
                    "type": "removal"
                })

            return explanations

        except Exception:
            logger.exception("Explanation building failed")
            return []

    # ---------------------------
    # 🔍 SMART ANALYSIS
    # ---------------------------
    @staticmethod
    def _analyze_change(old: str, new: str):
        old_clean = old.replace(" ", "")
        new_clean = new.replace(" ", "")

        # 🔹 formatting only
        if old_clean == new_clean:
            return {
                "change": "Code formatting improvement",
                "impact": "Improves readability and consistency",
                "type": "formatting"
            }

        # 🔹 overflow handling
        if "Math." in new and "Exact" in new:
            return {
                "change": "Added overflow-safe operation",
                "impact": "Prevents integer overflow at runtime",
                "type": "safety"
            }

        # 🔹 condition added
        if "if" in new and "if" not in old:
            return {
                "change": "Added conditional check",
                "impact": "Improves robustness and edge-case handling",
                "type": "logic"
            }

        # 🔹 fallback
        return {
            "change": "Updated logic implementation",
            "impact": "Improves correctness or performance",
            "type": "logic"
        }

    # ---------------------------
    # 🔍 NOISE FILTER
    # ---------------------------
    @staticmethod
    def _is_noise(line: str):
        line = line.strip()
        return line in {"{", "}", ";"} or not line

    # ---------------------------
    # 🔍 SMART SUMMARY
    # ---------------------------
    @staticmethod
    def _summarize_line(line: str):
        line = line.strip()

        if "throw" in line:
            return "Added exception handling"

        if "if" in line:
            return "Added validation condition"

        return f"Added code: {line}"