from ai_service import gemini_text
from config import get_settings


def summarize_text(text: str) -> str:
    settings = get_settings()
    text = text[: settings.max_input_chars]

    prompt = f"""
Summarize the following educational passage for a student.

Requirements:
- Keep the main ideas and important facts.
- Remove repetition and unnecessary detail.
- Use simple, clear language.
- Prefer a short paragraph followed by 3-7 key points when appropriate.
- Do not add information that is not supported by the passage.

PASSAGE:
{text}
"""
    return gemini_text(prompt)
