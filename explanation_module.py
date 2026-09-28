from functools import lru_cache

from ai_service import AIServiceError, gemini_text
from config import get_settings


@lru_cache(maxsize=1) 
def _load_local_pipeline():
    """
    Loads LaMini-Flan-T5 only when the Explain feature is first used.
    The model is downloaded and cached by Hugging Face.
    """
    from transformers import pipeline

    settings = get_settings()
    return pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        device=-1,
    )


def _local_explanation(topic: str) -> str:
    generator = _load_local_pipeline()
    prompt = (
        "Explain the following educational topic to a beginner in simple language. "
        "Use a short definition, 3-5 key points, and one easy example. "
        f"Topic: {topic}"
    )
    result = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False,
        truncation=True,
    )
    return result[0]["generated_text"].strip()


def _gemini_explanation(topic: str) -> str:
    prompt = f"""
Explain this topic to a beginner:
{topic}

Use:
1. A simple definition
2. 3-5 key points
3. One easy example
4. A one-line memory tip

Keep the explanation clear and concise.
"""
    return gemini_text(prompt)


def explain_topic(topic: str) -> str:
    settings = get_settings()

    if settings.explanation_backend == "gemini":
        return _gemini_explanation(topic)

    try:
        return _local_explanation(topic)
    except Exception as exc:
        if settings.explanation_fallback_to_gemini and settings.gemini_api_key:
            return _gemini_explanation(topic)
        raise AIServiceError(
            "The local LaMini explanation model could not be loaded. "
            "Install the requirements and ensure you have internet access for "
            "the first model download, or set EXPLANATION_BACKEND=gemini. "
            f"Original error: {exc}"
        ) from exc
