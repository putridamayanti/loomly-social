import json
import os

from fastapi import UploadFile

from google import genai
from starlette.concurrency import run_in_threadpool

import cloudinary.uploader
from app.core import settings, cloudinary as cloudinary_config
from app.schemas.content_schema import CaptionRequest, ChatRefinementRequest


class ContentService:
    async def analyze_media(self, file: UploadFile, payload: CaptionRequest):
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        try:
            # 2. Upload to Google's Files API (Free Tier)
            # This makes the file accessible to the Gemini model

            # 3. Initialize Gemini 1.5 Flash
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            uploaded_file = client.files.upload(file=temp_path)

            # model = genai.GenerativeModel("gemini-1.5-flash")

            # 4. Multimodal Prompt (The "Agent Assist" Logic)
            prompt = f"""
                Act as a Social Media Agent. 
                Analyze this image and create a {payload.tone} post for each platform: {str.join(', ', payload.platforms)}.
                Include:
                - A high-engagement caption.
                - 5 relevant hashtags.
                - 'Agent Logic': A short explanation of why this creative direction works.
                - Suggested posting time based on the content and target audience ({payload.target_audience}).
                - If {payload.include_emojis} is True, include relevant emojis in the caption.
                - The caption should be concise and optimized for engagement on the specified platforms.
                - suggested_time should be optimized for the specific platform.
                - suggested_time should be in ISO 8601 format.
                - Return the response for each platform in a structured format.
                - Output must match the schema: {{ "captions": [ {{ "tone": "", "content": "", "platform": "", "target_audience": "", "hashtags": [], "suggested_time": "" }} ] }}
                - ONLY RETURN THE RAW JSON WITHOUT ANY EXPLANATION OR ADDITIONAL TEXT.
                """

            # response = model.generate_content([uploaded_file, prompt])

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, prompt]
            )

            cleaned = str.replace(response.text, '```json', '')
            cleaned = str.replace(cleaned, '```', '')

            result = json.loads(cleaned)

            # Upload media to cloudinary for storage and future reference
            await file.seek(0)
            media = await run_in_threadpool(
                cloudinary.uploader.upload,
                file.file,
                folder="loomly"
            )

            return {
                "status": "success",
                "agent_output": response.text,
                "data": result,
                "media": media
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "An error occurred during chat refinement.",
                "error": str(e)
            }
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


    async def chat_refinement(self, payload: ChatRefinementRequest):
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            prompt = f"""
                You are a Social Media Assistant. The user previously generated these captions:
                {json.dumps(payload.previous_captions)}
                The user now says: "{payload.user_message}"
                Rules for refinement:
                - Return the updated list in the same JSON format as before.
                - ONLY RETURN THE RAW JSON WITHOUT ANY EXPLANATION OR ADDITIONAL TEXT.
                """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            cleaned = str.replace(response.text, '```json', '')
            cleaned = str.replace(cleaned, '```', '')

            result = json.loads(cleaned)

            return {
                "status": "success",
                # "agent_output": response.text,
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "An error occurred during chat refinement.",
                "error": str(e)
            }


content_service = ContentService()