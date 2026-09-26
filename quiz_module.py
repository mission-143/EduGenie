from ai_service import gemini_json
from schemas import QuizResponse


def generate_quiz(topic: str, num_questions: int = 5) -> dict:
    prompt = f"""
Create a {num_questions}-question educational multiple-choice quiz about:
{topic}

Rules:
- Each question must have exactly four options.
- correct_answer must exactly match one option.
- Include a short explanation for the correct answer.
- Keep the questions appropriate for learners.
- Avoid trick questions.
- Return only the requested structured data.
"""
    result = gemini_json(
        prompt,
        QuizResponse,
        system_instruction=(
            "You generate reliable educational quizzes. "
            "Always ensure each correct_answer exactly matches one of the four options."
        ),
    )
    return result.model_dump()
