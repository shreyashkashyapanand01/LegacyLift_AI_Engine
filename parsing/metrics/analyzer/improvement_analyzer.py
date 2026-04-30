class ImprovementAnalyzer:

    @staticmethod
    def analyze(comparison: dict, score: dict):
        """
        Convert metrics into human-readable insights
        """

        summary_parts = []
        improvements = []

        # ---------------------------
        # COMPLEXITY
        # ---------------------------
        if comparison["complexity_reduction"] > 0:
            improvements.append("Reduced cyclomatic complexity")
            summary_parts.append(
                f"complexity reduced by {comparison['complexity_reduction_pct']}%"
            )

        # ---------------------------
        # LOC
        # ---------------------------
        if comparison["loc_reduction"] > 0:
            improvements.append("Reduced code size")
            summary_parts.append(
                f"LOC reduced by {comparison['loc_reduction_pct']}%"
            )

        # ---------------------------
        # MAINTAINABILITY
        # ---------------------------
        if comparison["maintainability_improvement"] > 0:
            improvements.append("Improved maintainability")
            summary_parts.append(
                f"maintainability increased by {comparison['maintainability_improvement']}"
            )

        # ---------------------------
        # EFFORT
        # ---------------------------
        if comparison["effort_reduction"] > 0:
            improvements.append("Reduced computational effort")

        # ---------------------------
        # QUALITY LEVEL
        # ---------------------------
        after_score = score["after"]

        if after_score >= 85:
            quality_level = "Excellent"
        elif after_score >= 70:
            quality_level = "Good"
        elif after_score >= 50:
            quality_level = "Moderate"
        else:
            quality_level = "Poor"

        # ---------------------------
        # RISK DETECTION
        # ---------------------------
        if score["improvement"] < 0:
            risk = "Refactor degraded code quality"
        elif comparison["complexity_reduction"] < 0:
            risk = "Complexity increased"
        else:
            risk = "Low"

        # ---------------------------
        # CONFIDENCE
        # ---------------------------
        confidence = min(1.0, max(0.5, score["improvement"] / 50))

        # ---------------------------
        # FINAL SUMMARY
        # ---------------------------
        summary = "Code quality improved with " + ", ".join(summary_parts) if summary_parts else "No significant improvement detected"

        return {
            "summary": summary,
            "quality_level": quality_level,
            "key_improvements": improvements,
            "risk": risk,
            "confidence": round(confidence, 2)
        }