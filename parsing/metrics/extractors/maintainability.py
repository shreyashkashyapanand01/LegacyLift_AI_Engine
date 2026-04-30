import math


class MaintainabilityAnalyzer:

    @staticmethod
    def analyze(volume: float, complexity: int, loc: int):
        """
        Compute Maintainability Index (MI)
        """

        # ---------------------------
        # SAFETY CHECKS
        # ---------------------------
        if volume <= 0 or loc <= 0:
            return {"maintainability_index": 0}

        try:
            mi = (
                171
                - 5.2 * math.log(volume)
                - 0.23 * complexity
                - 16.2 * math.log(loc)
            )

            # normalize between 0–100
            mi = max(0, min(100, mi))

            return {
                "maintainability_index": round(mi, 2)
            }

        except Exception:
            return {"maintainability_index": 0}