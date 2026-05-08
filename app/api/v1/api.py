from fastapi import APIRouter
from app.api.v1.endpoints import *

api_router = APIRouter()

# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(medias.router, prefix="/medias", tags=["medias"])
api_router.include_router(users.router, prefix="/users", tags=["users"])