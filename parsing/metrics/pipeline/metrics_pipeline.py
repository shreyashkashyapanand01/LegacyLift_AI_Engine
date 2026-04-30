from parsing.metrics.feature_builder.feature_engineer import FeatureEngineer
from parsing.metrics.comparator.metrics_comparator import MetricsComparator
from parsing.metrics.scorer.quality_scorer import QualityScorer
from parsing.metrics.analyzer.improvement_analyzer import ImprovementAnalyzer
from parsing.metrics.models.metrics_schema import MetricsResult


class MetricsPipeline:

    @staticmethod
    def run(original_code: str, refactored_code: str, language: str):
        """
        Full metrics pipeline:
        code → features → comparison → scoring → analysis
        """

        try:
            # ---------------------------
            # STEP 1: FEATURE EXTRACTION
            # ---------------------------
            before_features = FeatureEngineer.build(original_code, language)
            after_features = FeatureEngineer.build(refactored_code, language)

            # safety check
            if not before_features or not after_features:
                return {"error": "Feature extraction failed"}

            # ---------------------------
            # STEP 2: COMPARISON
            # ---------------------------
            comparison = MetricsComparator.compare(before_features, after_features)

            # ---------------------------
            # STEP 3: QUALITY SCORING
            # ---------------------------
            score = QualityScorer.compare(before_features, after_features)

            # ---------------------------
            # STEP 4: HUMAN ANALYSIS
            # ---------------------------
            #analysis = ImprovementAnalyzer.analyze(comparison, score)
            
            analysis = ImprovementAnalyzer.analyze(
                comparison,
                score,
                before_features,
                after_features
            )

            # ---------------------------
            # FINAL OUTPUT
            # ---------------------------
            # return {
            #     "before": before_features,
            #     "after": after_features,
            #     "comparison": comparison,
            #     "score": score,
            #     "analysis": analysis
            # }
            
            return MetricsResult(
                before=before_features,
                after=after_features,
                comparison=comparison,
                score=score,
                analysis=analysis
            ).model_dump()

        except Exception as e:
            return {
                "error": str(e)
            }