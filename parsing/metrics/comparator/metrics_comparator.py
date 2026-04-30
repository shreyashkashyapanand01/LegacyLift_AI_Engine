class MetricsComparator:

    @staticmethod
    def _pct_change(before, after):
        if before == 0:
            return 0
        return round(((before - after) / before) * 100, 2)

    @staticmethod
    def compare(before: dict, after: dict):
        """
        Compare feature sets (before vs after)
        """

        # ---------------------------
        # COMPLEXITY
        # ---------------------------
        complexity_reduction = before["complexity"] - after["complexity"]

        # ---------------------------
        # LOC
        # ---------------------------
        loc_reduction = before["loc"] - after["loc"]

        # ---------------------------
        # MAINTAINABILITY
        # ---------------------------
        maintainability_improvement = (
            after["maintainability"] - before["maintainability"]
        )

        # ---------------------------
        # HALSTEAD
        # ---------------------------
        effort_before = before["halstead"]["effort"]
        effort_after = after["halstead"]["effort"]

        effort_reduction = effort_before - effort_after

        # ---------------------------
        # % CALCULATIONS
        # ---------------------------
        return {
            "complexity_reduction": complexity_reduction,
            "complexity_reduction_pct": MetricsComparator._pct_change(
                before["complexity"], after["complexity"]
            ),

            "loc_reduction": loc_reduction,
            "loc_reduction_pct": MetricsComparator._pct_change(
                before["loc"], after["loc"]
            ),

            "maintainability_improvement": round(maintainability_improvement, 2),

            "effort_reduction": round(effort_reduction, 2),
            "effort_reduction_pct": MetricsComparator._pct_change(
                effort_before, effort_after
            )
        }