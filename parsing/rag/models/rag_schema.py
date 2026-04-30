from pydantic import BaseModel
from typing import List, Optional, Dict


# ---------------------------
# 🔹 RETRIEVAL
# ---------------------------
class ResultItem(BaseModel):
    score: float
    code: str
    file: str
    function: str
    language: str


# ---------------------------
# 🔹 AGENT OUTPUTS
# ---------------------------
class AnalysisResponse(BaseModel):
    issues: List[str]
    patterns: List[str]
    suggestions: List[str]


class RefactorResponse(BaseModel):
    code: str
    changes: List[str]
    explanation: str


class TestResponse(BaseModel):
    unit_tests: List[str]
    edge_cases: List[str]


class ValidationResponse(BaseModel):
    is_valid: bool
    confidence: float
    errors: List[str]
    warnings: List[str]


# ---------------------------
# 🔥 MODULE 4 (REFRACTOR ENGINE)
# ---------------------------
class DiffItem(BaseModel):
    from_line: str
    to_line: str


class DiffResponse(BaseModel):
    added: List[str]
    removed: List[str]
    modified: List[Dict]   # flexible


class ExplanationItem(BaseModel):
    change: str
    impact: str
    type: str


class RefactorEngineResponse(BaseModel):
    language: str
    formatting_applied: bool
    original_code: str
    refactored_code: str
    diff: DiffResponse
    explanations: List[ExplanationItem]
    validation: Dict


# ---------------------------
# 🔥 MODULE 5 (EXECUTION ENGINE)
# ---------------------------
class ExecutionResultItem(BaseModel):
    status: str
    output: Optional[str] = None
    error: Optional[str] = None
    exception: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None


class ExecutionValidationResponse(BaseModel):
    status: str
    confidence: float
    summary: str
    failed_cases: List[Dict]

    original_results: Optional[List[ExecutionResultItem]] = None
    refactored_results: Optional[List[ExecutionResultItem]] = None


# ---------------------------
# 🔥 MODULE 6 (METRICS ENGINE)
# ---------------------------
class HalsteadResponse(BaseModel):
    volume: float
    difficulty: float
    effort: float


class FeatureResponse(BaseModel):
    complexity: int
    loc: int
    comment_lines: int
    maintainability: float
    halstead: HalsteadResponse


class MetricsComparisonResponse(BaseModel):
    complexity_reduction: float
    complexity_reduction_pct: float
    loc_reduction: float
    loc_reduction_pct: float
    maintainability_improvement: float
    effort_reduction: float
    effort_reduction_pct: float


class MetricsScoreResponse(BaseModel):
    before: float
    after: float
    improvement: float


class MetricsAnalysisResponse(BaseModel):
    summary: str
    quality_level: str
    key_improvements: List[str]
    risk: str
    confidence: float


class MetricsResponse(BaseModel):
    before: FeatureResponse
    after: FeatureResponse
    comparison: MetricsComparisonResponse
    score: MetricsScoreResponse
    analysis: MetricsAnalysisResponse


# ---------------------------
# 🔹 FINAL API RESPONSE
# ---------------------------
class RAGResponse(BaseModel):
    results: List[ResultItem]
    context: str

    analysis: Optional[AnalysisResponse] = None
    refactor: Optional[RefactorResponse] = None

    refactor_engine: Optional[RefactorEngineResponse] = None
    execution_validation: Optional[ExecutionValidationResponse] = None

    # 🔥 NEW (MODULE 6)
    metrics: Optional[MetricsResponse] = None

    tests: Optional[TestResponse] = None
    validation: Optional[ValidationResponse] = None