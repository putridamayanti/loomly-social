from datetime import datetime

from sqlmodel import SQLModel, Field

class Content(SQLModel, table=True):
    __tablename__ = "contents"

    id: str = Field(default=None, primary_key=True)
    topic: str = Field(default=None)
    media_id: str = Field(default=None, foreign_key="medias.id")
    content: str = Field(default=None)
    tone: str = Field(default=None) # e.g., "Professional", "Witty"
    target_audience: str = Field(default=None)
    platform: str = Field(default=None) # e.g., "Instagram", "Facebook", "Twitter"
    hashtags: str = Field(default=None) # Comma-separated hashtags
    suggested_time: datetime = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)