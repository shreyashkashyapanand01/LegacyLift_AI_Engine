from pydantic import BaseModel
from typing import List


# ---------------------------
# 🔹 HALSTEAD
# ---------------------------
class HalsteadMetrics(BaseModel):
    volume: float
    difficulty: float
    effort: float


# ---------------------------
# 🔹 FEATURE SET
# ---------------------------
class CodeFeatures(BaseModel):
    complexity: int
    loc: int
    comment_lines: int
    maintainability: float
    halstead: HalsteadMetrics


# ---------------------------
# 🔹 COMPARISON
# ---------------------------
class MetricsComparison(BaseModel):
    complexity_reduction: float
    complexity_reduction_pct: float
    loc_reduction: float
    loc_reduction_pct: float
    maintainability_improvement: float
    effort_reduction: float
    effort_reduction_pct: float


# ---------------------------
# 🔹 QUALITY SCORE
# ---------------------------
class QualityScore(BaseModel):
    before: float
    after: float
    improvement: float


# ---------------------------
# 🔹 ANALYSIS
# ---------------------------
class MetricsAnalysis(BaseModel):
    summary: str
    quality_level: str
    key_improvements: List[str]
    risk: str
    confidence: float


# ---------------------------
# 🔹 FINAL METRICS OBJECT
# ---------------------------
class MetricsResult(BaseModel):
    before: CodeFeatures
    after: CodeFeatures
    comparison: MetricsComparison
    score: QualityScore
    analysis: MetricsAnalysis