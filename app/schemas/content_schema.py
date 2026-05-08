from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel

class BrandVoiceRequest(BaseModel):
    tone: str
    target_audience: str
    include_emojis: Optional[bool] = False

class CaptionRequest(BaseModel):
    tone: str
    target_audience: str
    include_emojis: Optional[bool] = False
    platforms: List[str]

class CaptionResponseItem(BaseModel):
    tone: str
    target_audience: str
    platform: str
    content: str
    hashtags: Optional[List[str]] = None
    suggested_time: datetime

class CaptionResponse(BaseModel):
    captions: List[CaptionResponseItem]

class ChatRefinementRequest(BaseModel):
    user_message: str
    previous_captions: list[Any]