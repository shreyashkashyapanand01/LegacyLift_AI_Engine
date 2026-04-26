# from pydantic import BaseModel
# from typing import List


# class RAGResult(BaseModel):
#     score: float
#     code: str
#     file: str
#     function: str
#     language: str


# class RAGResponse(BaseModel):
#     results: List[RAGResult]
#     context: str
#     answer: str 


# from pydantic import BaseModel
# from typing import List


# class ResultItem(BaseModel):
#     score: float
#     code: str
#     file: str
#     function: str
#     language: str


# class Answer(BaseModel):
#     explanation: str
#     code_reference: str
#     examples: List[str]


# class RAGResponse(BaseModel):
#     results: List[ResultItem]
#     context: str
#     answer: Answer

from pydantic import BaseModel
from typing import List, Optional


class ResultItem(BaseModel):
    score: float
    code: str
    file: str
    function: str
    language: str


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


class RAGResponse(BaseModel):
    results: List[ResultItem]
    context: str

    analysis: Optional[AnalysisResponse] = None
    refactor: Optional[RefactorResponse] = None
    tests: Optional[TestResponse] = None
    validation: Optional[ValidationResponse] = None