from ai_service import gemini_json
from schemas import LearningPathResponse


def recommend_learning_path(
    topic: str,
    current_level: str,
    goal: str,
) -> dict:
    prompt = f"""
Create a practical learning path for the topic "{topic}".

Learner level: {current_level}
Learner goal: {goal}

Create 5 to 7 ordered steps from the learner's current level toward the goal.
Each step must contain:
- a clear title
- a simple description
- one practical practice task

Do not assume the learner already knows advanced prerequisites.
"""
    result = gemini_json(
        prompt,
        LearningPathResponse,
        system_instruction=(
            "You are a supportive educational planner. "
            "Make learning paths realistic, progressive, and actionable."
        ),
    )
    data = result.model_dump()
    data["topic"] = topic
    data["current_level"] = current_level
    data["goal"] = goal
    return data
