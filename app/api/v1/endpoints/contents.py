from fastapi import APIRouter, UploadFile, File, Form, Body
from starlette import status

from app.schemas.content_schema import CaptionRequest, CaptionResponseItem, ChatRefinementRequest
from app.schemas.response_schema import ResponseSchema
from app.services import content_service

router = APIRouter()

@router.post("/generate-caption", tags=["contents"])
async def generate_caption(
        tone: str = Form(...),
        target_audience: str = Form(...),
        platforms: str = Form(...),
        include_emojis: str = Form(...),
        file: UploadFile = File(...)
):
    platforms = str.split(platforms, ',')
    include_emojis = True if include_emojis.lower() == 'true' else False

    payload = CaptionRequest(
        tone=tone,
        target_audience=target_audience,
        platforms=platforms,
        include_emojis=include_emojis
    )
    result = await content_service.analyze_media(file, payload)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Content generated successfully", data=result)


@router.post("/chat-refinement", tags=["contents"])
async def chat_refinement(request: ChatRefinementRequest = Body(...)):
    result = await content_service.chat_refinement(request)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Chat refinement successful", data=result)