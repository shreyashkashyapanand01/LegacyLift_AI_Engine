# class ImprovementAnalyzer:

#     @staticmethod
#     def analyze(comparison: dict, score: dict):
#         """
#         Convert metrics into human-readable insights
#         """

#         summary_parts = []
#         improvements = []

#         # ---------------------------
#         # COMPLEXITY
#         # ---------------------------
#         if comparison["complexity_reduction"] > 0:
#             improvements.append("Reduced cyclomatic complexity")
#             summary_parts.append(
#                 f"complexity reduced by {comparison['complexity_reduction_pct']}%"
#             )

#         # ---------------------------
#         # LOC
#         # ---------------------------
#         if comparison["loc_reduction"] > 0:
#             improvements.append("Reduced code size")
#             summary_parts.append(
#                 f"LOC reduced by {comparison['loc_reduction_pct']}%"
#             )

#         # ---------------------------
#         # MAINTAINABILITY
#         # ---------------------------
#         if comparison["maintainability_improvement"] > 0:
#             improvements.append("Improved maintainability")
#             summary_parts.append(
#                 f"maintainability increased by {comparison['maintainability_improvement']}"
#             )

#         # ---------------------------
#         # EFFORT
#         # ---------------------------
#         if comparison["effort_reduction"] > 0:
#             improvements.append("Reduced computational effort")

#         # ---------------------------
#         # QUALITY LEVEL
#         # ---------------------------
#         after_score = score["after"]

#         if after_score >= 85:
#             quality_level = "Excellent"
#         elif after_score >= 70:
#             quality_level = "Good"
#         elif after_score >= 50:
#             quality_level = "Moderate"
#         else:
#             quality_level = "Poor"

#         # ---------------------------
#         # RISK DETECTION
#         # ---------------------------
#         if score["improvement"] < 0:
#             risk = "Refactor degraded code quality"
#         elif comparison["complexity_reduction"] < 0:
#             risk = "Complexity increased"
#         else:
#             risk = "Low"

#         # ---------------------------
#         # CONFIDENCE
#         # ---------------------------
#         confidence = min(1.0, max(0.5, score["improvement"] / 50))

#         # ---------------------------
#         # FINAL SUMMARY
#         # ---------------------------
#         summary = "Code quality improved with " + ", ".join(summary_parts) if summary_parts else "No significant improvement detected"

#         return {
#             "summary": summary,
#             "quality_level": quality_level,
#             "key_improvements": improvements,
#             "risk": risk,
#             "confidence": round(confidence, 2)
#         }



class ImprovementAnalyzer:

    @staticmethod
    def _detect_safety_improvement(before: dict, after: dict) -> bool:
        """
        Detect basic safety improvements (heuristic)
        """
        # Heuristic: effort increase + no degradation in correctness metrics
        # (we don't have execution data here, so keep it safe)

        # If effort increased significantly, assume added safety logic
        effort_change = after["halstead"]["effort"] - before["halstead"]["effort"]

        if effort_change > 100:
            return True

        return False

    @staticmethod
    def analyze(comparison: dict, score: dict, before: dict, after: dict):
        """
        Convert metrics into human-readable insights (ENHANCED)
        """

        summary_parts = []
        improvements = []
        tradeoffs = []

        # ---------------------------
        # COMPLEXITY
        # ---------------------------
        if comparison["complexity_reduction"] > 0:
            improvements.append("Reduced cyclomatic complexity")
            summary_parts.append(
                f"complexity reduced by {comparison['complexity_reduction_pct']}%"
            )
        elif comparison["complexity_reduction"] < 0:
            tradeoffs.append("Increased complexity")

        # ---------------------------
        # LOC
        # ---------------------------
        if comparison["loc_reduction"] > 0:
            improvements.append("Reduced code size")
            summary_parts.append(
                f"LOC reduced by {comparison['loc_reduction_pct']}%"
            )
        elif comparison["loc_reduction"] < 0:
            tradeoffs.append("Increased code size")

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
        elif comparison["effort_reduction"] < 0:
            tradeoffs.append("Increased computational effort")

        # ---------------------------
        # SAFETY DETECTION (NEW 🔥)
        # ---------------------------
        safety_improved = ImprovementAnalyzer._detect_safety_improvement(before, after)

        if safety_improved:
            improvements.append("Improved numerical safety and robustness")

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
        if score["improvement"] < 0 and not safety_improved:
            risk = "Refactor degraded code quality"
        elif score["improvement"] < 0 and safety_improved:
            risk = "Trade-off: safety improved but efficiency reduced"
        elif comparison["complexity_reduction"] < 0:
            risk = "Complexity increased"
        else:
            risk = "Low"

        # ---------------------------
        # CONFIDENCE
        # ---------------------------
        confidence = min(1.0, max(0.5, abs(score["improvement"]) / 50))

        # ---------------------------
        # FINAL SUMMARY (ENHANCED 🔥)
        # ---------------------------
        if improvements and not tradeoffs:
            summary = "Code quality improved with " + ", ".join(summary_parts)
        elif improvements and tradeoffs:
            summary = (
                "Code shows mixed impact: "
                + ", ".join(improvements)
                + " but also "
                + ", ".join(tradeoffs)
            )
        else:
            summary = "No significant improvement detected"

        return {
            "summary": summary,
            "quality_level": quality_level,
            "key_improvements": improvements,
            "risk": risk,
            "confidence": round(confidence, 2)
        }