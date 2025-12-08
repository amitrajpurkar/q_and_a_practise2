from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render the main quiz page with topic/difficulty selection.

    Full behavior (loading topics, wiring HTMX) will be implemented in later phases.
    """

    return templates.TemplateResponse("quiz.html", {"request": request})


@router.post("/api/quiz/start")
async def start_quiz() -> JSONResponse:
    """Stub endpoint for starting a quiz session.

    Full logic will be added in the User Story 1 phase.
    """

    return JSONResponse({"detail": "start_quiz not implemented yet"})


@router.post("/api/quiz/{session_id}/answer")
async def submit_answer(session_id: str) -> JSONResponse:
    """Stub endpoint for submitting an answer.

    Full logic will be added in the User Story 1 phase.
    """

    return JSONResponse({"detail": "submit_answer not implemented yet", "session_id": session_id})


@router.get("/api/quiz/{session_id}/summary")
async def get_summary(session_id: str) -> JSONResponse:
    """Stub endpoint for retrieving quiz summary.

    Full logic will be added in later phases for summary and review.
    """

    return JSONResponse({"detail": "get_summary not implemented yet", "session_id": session_id})
