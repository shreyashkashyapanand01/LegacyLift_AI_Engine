from fastapi import APIRouter, UploadFile, File

from parsing.api.services.parse_service import ParseService

router = APIRouter()
service = ParseService()


@router.post("/parse")
async def parse_code(file: UploadFile = File(...)):
    return await service.parse(file)