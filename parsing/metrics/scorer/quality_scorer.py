class QualityScorer:

    @staticmethod
    def _normalize(value, max_value):
        if max_value == 0:
            return 0
        return min(value / max_value, 1)

    @staticmethod
    def _inverse_normalize(value, max_value):
        """
        For metrics where LOWER is better
        """
        if max_value == 0:
            return 1
        return 1 - min(value / max_value, 1)

    @staticmethod
    def compute(features: dict):
        """
        Compute quality score (0–100)
        """

        # ---------------------------
        # EXTRACT METRICS
        # ---------------------------
        complexity = features["complexity"]
        loc = features["loc"]
        maintainability = features["maintainability"]
        effort = features["halstead"]["effort"]

        # ---------------------------
        # NORMALIZATION LIMITS
        # (heuristic but practical)
        # ---------------------------
        MAX_COMPLEXITY = 10
        MAX_LOC = 50
        MAX_EFFORT = 1000

        # ---------------------------
        # NORMALIZE
        # ---------------------------
        complexity_score = QualityScorer._inverse_normalize(complexity, MAX_COMPLEXITY)
        loc_score = QualityScorer._inverse_normalize(loc, MAX_LOC)
        effort_score = QualityScorer._inverse_normalize(effort, MAX_EFFORT)

        maintainability_score = maintainability / 100  # already normalized

        # ---------------------------
        # WEIGHTS
        # ---------------------------
        weights = {
            "complexity": 0.3,
            "loc": 0.2,
            "maintainability": 0.3,
            "effort": 0.2
        }

        # ---------------------------
        # FINAL SCORE
        # ---------------------------
        score = (
            complexity_score * weights["complexity"]
            + loc_score * weights["loc"]
            + maintainability_score * weights["maintainability"]
            + effort_score * weights["effort"]
        )

        return round(score * 100, 2)

    # ---------------------------
    # COMPARE SCORES
    # ---------------------------
    @staticmethod
    def compare(before: dict, after: dict):
        before_score = QualityScorer.compute(before)
        after_score = QualityScorer.compute(after)

        return {
            "before": before_score,
            "after": after_score,
            "improvement": round(after_score - before_score, 2)
        }