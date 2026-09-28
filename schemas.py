from typing import Literal

from pydantic import BaseModel, Field 


class QARequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)


class QuizRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=3000)
    num_questions: int = Field(default=5, ge=1, le=10)


class SummaryRequest(BaseModel):
    text: str = Field(min_length=20, max_length=12000)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)
    current_level: Literal["Beginner", "Intermediate", "Advanced"] = "Beginner"
    goal: str = Field(default="Understand the topic well", max_length=2000)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class LearningStep(BaseModel):
    step: int
    title: str
    description: str
    practice_task: str


class LearningPathResponse(BaseModel):
    topic: str
    current_level: str
    goal: str
    steps: list[LearningStep]
