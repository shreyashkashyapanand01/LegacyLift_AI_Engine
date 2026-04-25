from pydantic import BaseModel
from typing import List


# ---------------------------
# FUNCTION SCHEMA
# ---------------------------
class FunctionSchema(BaseModel):
    id: str
    function: str
    file: str
    line: int
    end_line: int
    type: str
    language: str
    code: str  # 🔥 important for RAG


# ---------------------------
# DEPENDENCY SCHEMA
# ---------------------------
class DependencySchema(BaseModel):
    source: str
    target: str
    type: str
    language: str


# ---------------------------
# FINAL OUTPUT
# ---------------------------
class ParsingOutput(BaseModel):
    project: str
    files: List[dict]
    functions: List[FunctionSchema]
    dependencies: List[DependencySchema]