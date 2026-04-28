import logging

logger = logging.getLogger(__name__)


class OutputComparator:

    # ---------------------------
    # 🚀 MAIN COMPARATOR
    # ---------------------------
    @staticmethod
    def compare(original_results: list, refactored_results: list):
        try:
            total = len(original_results)
            passed = 0
            improved = 0
            failed_cases = []

            for i in range(total):
                orig = original_results[i]
                ref = refactored_results[i]

                decision = OutputComparator._compare_single(orig, ref)

                if decision["status"] == "PASS":
                    passed += 1
                elif decision["status"] == "IMPROVED":
                    passed += 1
                    improved += 1
                else:
                    failed_cases.append({
                        "test_index": i,
                        "original": orig,
                        "refactored": ref,
                        "reason": decision["reason"]
                    })

            # ---------------------------
            # 📊 FINAL STATUS
            # ---------------------------
            status = "PASS" if len(failed_cases) == 0 else "FAIL"

            confidence = passed / total if total > 0 else 0

            summary = OutputComparator._build_summary(
                total, passed, improved, failed_cases
            )

            return {
                "status": status,
                "confidence": round(confidence, 2),
                "summary": summary,
                "failed_cases": failed_cases
            }

        except Exception:
            logger.exception("Comparison failed")

            return {
                "status": "ERROR",
                "confidence": 0,
                "summary": "Comparator failed",
                "failed_cases": []
            }

    # ---------------------------
    # 🔍 SINGLE TEST COMPARISON
    # ---------------------------
    @staticmethod
    def _compare_single(orig: dict, ref: dict):

        # ---------------------------
        # BOTH PASS
        # ---------------------------
        if orig["status"] == "PASS" and ref["status"] == "PASS":
            if orig.get("output") == ref.get("output"):
                return {"status": "PASS"}
            else:
                return {
                    "status": "FAIL",
                    "reason": "Output mismatch"
                }

        # ---------------------------
        # BOTH FAIL (same behavior)
        # ---------------------------
        if orig["status"] == "FAIL" and ref["status"] == "FAIL":
            return {"status": "PASS"}

        # ---------------------------
        # REFACTOR FIXED FAILURE
        # ---------------------------
        if orig["status"] != "PASS" and ref["status"] == "PASS":
            return {
                "status": "IMPROVED",
                "reason": "Refactor fixed failing case"
            }

        # ---------------------------
        # REFACTOR BROKE WORKING CODE ❌
        # ---------------------------
        if orig["status"] == "PASS" and ref["status"] != "PASS":
            return {
                "status": "FAIL",
                "reason": "Refactor broke working behavior"
            }

        # ---------------------------
        # DEFAULT FAIL
        # ---------------------------
        return {
            "status": "FAIL",
            "reason": "Unexpected mismatch"
        }

    # ---------------------------
    # 🧠 SUMMARY BUILDER
    # ---------------------------
    @staticmethod
    def _build_summary(total, passed, improved, failed_cases):

        if not failed_cases:
            if improved > 0:
                return f"All tests passed. {improved} cases improved by refactor."
            return "All tests passed successfully."

        return f"{len(failed_cases)} test(s) failed. Refactor introduced issues."