
# Offline Quiz Question Bank

## Summary

This project is a minimal offline web-based quiz application built with Python and FastAPI. It uses a local CSV question bank so a student can:

- Choose a **topic/subject** and a **difficulty level** (easy, medium, hard).
- Answer a fixed set of 10 multiple-choice questions matching that topic and difficulty.
- Receive **per-question feedback** (correct/incorrect).
- See an **end-of-quiz summary** with totals, percentage score, and time spent.
- Review **incorrect questions** with both the chosen and correct answers.

It is intentionally small but layered to support IB Computer Science SL concepts: clear domain models, a service layer, HTTP routes, templates, and basic tests.

## Architecture Overview

The application uses a classic layered structure over a local CSV file.

```text
+-----------------------------+
|          Browser            |
|  (HTML, CSS, minimal JS)    |
+--------------+--------------+
               |
               v
+--------------+--------------+
|          FastAPI API        |
|      src/api/routes.py      |
+--------------+--------------+
               |
               v
+--------------+-----------------------------+
|           Quiz Service Layer               |
|      src/services/quiz_service.py          |
+--------------+-----------------------------+
               |
     +---------+-----------+----------------------+
     |                     |                      |
     v                     v                      v
+-----------+    +----------------+    +---------------------------+
|  Models   |    |     Utils      |    |   CSV Question Bank       |
| src/models|    |  src/utils/*   |    | src/data/question-bank.csv|
+-----------+    +----------------+    +---------------------------+
```

High-level responsibilities:

- `src/models/` – question, attempt, and quiz session data structures.
- `src/services/quiz_service.py` – CSV loading, session management, scoring, and summaries.
- `src/api/routes.py` – FastAPI routes for starting quizzes, submitting answers, and viewing summaries.
- `src/web/templates/` – Jinja2 templates for the UI.
- `src/utils/timing.py` – timing helpers.
- `tests/unit/test_quiz_service.py` – unit tests for quiz logic and summaries.

## Static Code Analysis

*(Values are based on simple file and line counts within this repository.)*

### Python files (`src/` and `tests/`)

| File                              | Lines |
|-----------------------------------|------:|
| `src/main.py`                     |   20 |
| `src/api/routes.py`               |  160 |
| `src/services/quiz_service.py`    |  257 |
| `src/models/question.py`          |   69 |
| `src/utils/timing.py`             |   18 |
| `src/__init__.py`                 |    0 |
| `src/api/__init__.py`             |    0 |
| `src/models/__init__.py`          |    0 |
| `src/services/__init__.py`        |    0 |
| `src/utils/__init__.py`           |    0 |
| `tests/unit/test_quiz_service.py` |  105 |
| **Total**                         | **629** |

### HTML templates

| File                          |
|-------------------------------|
| `src/web/templates/base.html` |
| `src/web/templates/quiz.html` |

### Static assets

| Type | File                              |
|------|-----------------------------------|
| CSS  | `src/web/static/css/tailwind.css` |
| JS   | `src/web/static/js/htmx.min.js`   |

## Running the Application

### Prerequisites

- Python 3.12
- [`uv`](https://github.com/astral-sh/uv) (Astral) installed

From the project root:

```bash
# 1. Create and activate a virtual environment
uv venv
source .venv/bin/activate  # or your platform equivalent

# 2. Install dependencies
uv pip install fastapi uvicorn pandas jinja2 pydantic

# 3. Ensure the question bank CSV exists
#    Example path (you already have a populated file):
#    src/data/question-bank.csv

# 4. Start the application
uv run uvicorn src.main:app --reload

# 5. Open the app in your browser
#    http://127.0.0.1:8000/
```

On the home page, select a topic and difficulty, start a quiz, answer questions, and then review your summary and incorrect answers at the end.

