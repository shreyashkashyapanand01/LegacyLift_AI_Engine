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
    modified: List[Dict]   # keeping flexible (your structure)


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
    validation: Dict   # you already return {is_valid, errors}


# ---------------------------
# 🔹 FINAL API RESPONSE
# ---------------------------
class RAGResponse(BaseModel):
    results: List[ResultItem]
    context: str

    analysis: Optional[AnalysisResponse] = None
    refactor: Optional[RefactorResponse] = None

    # 🔥 NEW FIELD
    refactor_engine: Optional[RefactorEngineResponse] = None

    tests: Optional[TestResponse] = None
    validation: Optional[ValidationResponse] = None