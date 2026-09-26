import json
from functools import lru_cache
from typing import Any, Type

from config import get_settings

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover
    genai = None
    types = None


class AIServiceError(RuntimeError):
    """Raised when an AI backend is misconfigured or fails to respond."""


@lru_cache(maxsize=1)
def _get_client():
    settings = get_settings()
    if not settings.gemini_api_key:
        raise AIServiceError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )
    if genai is None:
        raise AIServiceError(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        )
    return genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(
            timeout=int(settings.gemini_timeout_seconds * 1000)
        ),
    )


def gemini_text(prompt: str, system_instruction: str | None = None) -> str:
    settings = get_settings()
    client = _get_client()

    config_kwargs = {}
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    text = getattr(response, "text", None)
    if not text:
        raise AIServiceError("Gemini returned an empty response.")
    return text.strip()


def gemini_json(
    prompt: str,
    schema_model: Type[Any],
    system_instruction: str | None = None,
) -> Any:
    settings = get_settings()
    client = _get_client()

    config_kwargs = {
        "response_mime_type": "application/json",
        "response_schema": schema_model,
    }
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    raw = getattr(response, "text", None)
    if not raw:
        raise AIServiceError("Gemini returned an empty JSON response.")

    try:
        return schema_model.model_validate_json(raw)
    except Exception:
        # Defensive fallback for older/variant SDK responses.
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1).replace("```", "", 1).strip()
        return schema_model.model_validate(json.loads(cleaned))
