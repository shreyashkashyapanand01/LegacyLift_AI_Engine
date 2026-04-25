from pydantic import BaseModel
from typing import List


class RAGResult(BaseModel):
    score: float
    code: str
    file: str
    function: str
    language: str


class RAGResponse(BaseModel):
    results: List[RAGResult]
    context: str