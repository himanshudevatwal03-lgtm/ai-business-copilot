import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PROJECT_NAME: str = "AI Business Copilot"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./copilot_erp.db")
    
    # Inference configuration:
    # "local" (default deterministic analytics engine, 0 external keys required)
    # "cloud" (OpenAI / Gemini compatible provider)
    # "qualcomm" (Phase 2 Snapdragon NPU integration adapter)
    INFERENCE_PROVIDER: str = os.getenv("INFERENCE_PROVIDER", "local")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "*"
    ]

settings = Settings()
