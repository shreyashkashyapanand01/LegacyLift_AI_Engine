from parsing.metrics.analyzer.improvement_analyzer import ImprovementAnalyzer

comparison = {
    "complexity_reduction": 2,
    "complexity_reduction_pct": 66.67,
    "loc_reduction": 2,
    "loc_reduction_pct": 40.0,
    "maintainability_improvement": 20,
    "effort_reduction": 200
}

score = {
    "before": 70,
    "after": 86.8,
    "improvement": 16.8
}

print(ImprovementAnalyzer.analyze(comparison, score))