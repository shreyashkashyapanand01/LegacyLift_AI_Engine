from pydantic import BaseModel, Field
from typing import List, Optional


# ---------------------------
# 🔍 ANALYSIS OUTPUT
# ---------------------------
class Analysis(BaseModel):
    issues: List[str] = Field(default_factory=list)
    patterns: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


# ---------------------------
# 🔧 REFACTOR OUTPUT
# ---------------------------
class Refactor(BaseModel):
    code: str = ""
    changes: List[str] = Field(default_factory=list)
    explanation: Optional[str] = ""


# ---------------------------
# 🧪 TEST OUTPUT
# ---------------------------
class TestCases(BaseModel):
    unit_tests: List[str] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)


# ---------------------------
# ✅ VALIDATION OUTPUT
# ---------------------------
# class Validation(BaseModel):
#     is_valid: bool = False
#     confidence: float = 0.0
#     errors: List[str] = Field(default_factory=list)
    
class Validation(BaseModel):
    is_valid: bool = False
    confidence: float = 0.0
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)   # 🔥 NEW


# ---------------------------
# 🧠 GLOBAL STATE
# ---------------------------
class AgentState(BaseModel):
    query: str
    context: str
    language: Optional[str] = None

    analysis: Optional[Analysis] = None
    refactor: Optional[Refactor] = None
    tests: Optional[TestCases] = None
    validation: Optional[Validation] = None
    
    retry_count: int = 0