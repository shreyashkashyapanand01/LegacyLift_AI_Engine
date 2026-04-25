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


from pydantic import BaseModel
from typing import List


class ResultItem(BaseModel):
    score: float
    code: str
    file: str
    function: str
    language: str


class Answer(BaseModel):
    explanation: str
    code_reference: str
    examples: List[str]


class RAGResponse(BaseModel):
    results: List[ResultItem]
    context: str
    answer: Answer