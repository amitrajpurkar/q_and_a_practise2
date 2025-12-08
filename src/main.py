from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes import router as api_router


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static files (CSS, JS) under /static
static_dir = BASE_DIR / "web" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include API and page routes
app.include_router(api_router)
