from pydantic import BaseModel
from typing import List, Optional


class LineChange(BaseModel):
    type: str              # added / removed / modified
    original: Optional[str] = None
    new: Optional[str] = None


class DiffResult(BaseModel):
    summary: str
    line_changes: List[LineChange]


class ExplanationItem(BaseModel):
    change: str
    reason: str
    impact: str


class RefactorEngineOutput(BaseModel):
    original_code: str
    refactored_code: str
    language: str

    diff: DiffResult
    explanations: List[ExplanationItem]

    is_valid: bool
    formatting_applied: bool