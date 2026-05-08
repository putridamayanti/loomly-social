import enum
from datetime import datetime

from sqlmodel import SQLModel, Field


class MediaType(enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

class Media(SQLModel, table=True):
    __tablename__ = "medias"

    id: str = Field(default=None, primary_key=True)
    url: str
    format: str = Field(default=None)
    size: int = Field(default=None)
    public_id: str = Field(default=None)
    type: MediaType

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)