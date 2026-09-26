from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
)
from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request,name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return {"answer": answer_question(payload.question)}


@app.post("/explain")
async def explain(payload: ExplainRequest):
    return {"explanation": explain_topic(payload.topic)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"quiz": generate_quiz(payload.topic, payload.num_questions)}


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: LearningPathRequest):
    return {
        "recommendations": recommend_learning_path(
            topic=payload.topic,
            current_level=payload.current_level,
            goal=payload.goal,
        )
    }
