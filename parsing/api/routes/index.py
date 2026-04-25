from fastapi import APIRouter, UploadFile, File
import shutil
import os

from parsing.api.services.rag_service import RagService

router = APIRouter()
service = RagService()


@router.post("/index")
async def index_project(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job_id = service.index_project(temp_path)

    os.remove(temp_path)

    return {
        "message": "Indexing successful",
        "job_id": job_id
    }