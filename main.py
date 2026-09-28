import logging 
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
from ai_service import AIServiceError
from config import get_settings

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("edugenie")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-powered educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


@app.exception_handler(AIServiceError)
async def ai_service_error_handler(request: Request, exc: AIServiceError):
    logger.error("AI service error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "The AI service is temporarily unavailable. Please try again later."},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong while processing your request."},
    )

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
def qa(payload: QARequest):
    return {"answer": answer_question(payload.question)}


@app.post("/explain")
def explain(payload: ExplainRequest):
    return {"explanation": explain_topic(payload.topic)}


@app.post("/quiz")
def quiz(payload: QuizRequest):
    return {"quiz": generate_quiz(payload.topic, payload.num_questions)}


@app.post("/summarize")
def summarize(payload: SummaryRequest):
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
def learning_recommendations(payload: LearningPathRequest):
    return {
        "recommendations": recommend_learning_path(
            topic=payload.topic,
            current_level=payload.current_level,
            goal=payload.goal,
        )
    }
