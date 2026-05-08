import cloudinary.uploader
from app.core import cloudinary as cloudinary_config
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool

class MediaService:
    async def upload_media(self, file: UploadFile):
        result = await run_in_threadpool(
            cloudinary.uploader.upload, 
            file.file, 
            folder="loomly"
        )
        return result


media_service = MediaService()