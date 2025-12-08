from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.services import quiz_service


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render the main quiz page with topic/difficulty selection."""

    try:
        topics = quiz_service.get_available_topics()
        difficulties = quiz_service.get_available_difficulties()
        load_error = None
    except Exception as exc:  # pragma: no cover - defensive
        topics = []
        difficulties = []
        load_error = str(exc)

    context = {
        "request": request,
        "topics": topics,
        "difficulties": difficulties,
        "load_error": load_error,
        "session_id": None,
        "question": None,
        "last_result": None,
        "summary": None,
    }
    return templates.TemplateResponse("quiz.html", context)


@router.post("/api/quiz/start", response_class=HTMLResponse)
async def start_quiz(
    request: Request,
    topic: str = Form(...),
    difficulty: str = Form(...),
) -> HTMLResponse:
    """Start a new quiz session for the chosen topic and difficulty."""

    try:
        session = quiz_service.create_quiz_session(topic, difficulty)
    except ValueError as exc:
        topics = quiz_service.get_available_topics()
        difficulties = quiz_service.get_available_difficulties()
        context = {
            "request": request,
            "topics": topics,
            "difficulties": difficulties,
            "load_error": str(exc),
            "session_id": None,
            "question": None,
            "last_result": None,
            "summary": None,
        }
        return templates.TemplateResponse("quiz.html", context, status_code=400)

    question = quiz_service.get_next_question(session.id)

    context = {
        "request": request,
        "topics": quiz_service.get_available_topics(),
        "difficulties": quiz_service.get_available_difficulties(),
        "load_error": None,
        "session_id": session.id,
        "question": question,
        "last_result": None,
        "summary": None,
    }
    return templates.TemplateResponse("quiz.html", context)


@router.post("/api/quiz/{session_id}/answer", response_class=HTMLResponse)
async def submit_answer(
    request: Request,
    session_id: str,
    question_id: str = Form(...),
    chosen_option: str = Form(...),
) -> HTMLResponse:
    """Submit an answer and return the next question (or finished state)."""

    try:
        correct, next_question, finished = quiz_service.record_answer(
            session_id,
            question_id,
            chosen_option,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    last_result = {"correct": correct, "finished": finished}
    summary = None
    if finished:
        summary = quiz_service.compute_quiz_summary(session_id)

    context = {
        "request": request,
        "topics": quiz_service.get_available_topics(),
        "difficulties": quiz_service.get_available_difficulties(),
        "load_error": None,
        "session_id": session_id,
        "question": next_question,
        "last_result": last_result,
        "summary": summary,
    }
    return templates.TemplateResponse("quiz.html", context)


@router.get("/api/quiz/{session_id}/summary")
async def get_summary(session_id: str) -> JSONResponse:
    """Stub endpoint for retrieving quiz summary.

    Full logic will be added in later phases for summary and review.
    """

    summary = quiz_service.compute_quiz_summary(session_id)
    return JSONResponse(summary)
