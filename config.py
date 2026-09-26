import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.getenv(
        "APP_NAME", "EduGenie - Google Gemini Powered Learning Assistant"
    )
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
    explanation_backend: str = os.getenv(
        "EXPLANATION_BACKEND", "local"
    ).strip().lower()
    explanation_fallback_to_gemini: bool = (
        os.getenv("EXPLANATION_FALLBACK_TO_GEMINI", "true").strip().lower()
        in {"1", "true", "yes", "y"}
    )
    local_model_name: str = os.getenv(
        "LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M"
    ).strip()
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "12000"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")


@lru_cache
def get_settings() -> Settings:
    return Settings()
