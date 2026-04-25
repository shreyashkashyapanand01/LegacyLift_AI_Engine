from fastapi import APIRouter
from pydantic import BaseModel

from parsing.api.services.rag_service import RagService
from parsing.rag.models.rag_schema import RAGResponse

router = APIRouter()
service = RagService()


class QueryRequest(BaseModel):
    job_id: str
    query: str
    top_k: int = 3


@router.post("/query", response_model=RAGResponse)
def query_code(req: QueryRequest):
    return service.query(
        job_id=req.job_id,
        query=req.query,
        top_k=req.top_k
    )