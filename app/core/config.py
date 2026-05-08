from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    PROJECT_NAME: str = "MindNest Backend"
    APP_TITLE: str = "Mindnest v1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = ""
    DATABASE_SSL_CA_FILE: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_DEFAULT_MODEL: str = "gemini-3-flash-preview"
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    class Config:
        env_file = ".env"

settings = Setting()