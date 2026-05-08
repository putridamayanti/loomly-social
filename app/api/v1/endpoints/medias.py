from fastapi import APIRouter, UploadFile, File
from starlette import status

from app.schemas.response_schema import ResponseSchema
from app.services import media_service

router = APIRouter()

@router.post("/upload", tags=["medias"])
async def upload_media(file: UploadFile = File(...)):
    result = await media_service.upload_media(file)
    return ResponseSchema(status_code=status.HTTP_201_CREATED, detail="Upload success", data=result)