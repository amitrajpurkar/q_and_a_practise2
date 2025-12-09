# Offline Quiz Application Architecture

## Overview

This project is a minimal offline web-based quiz application built with Python and FastAPI. It is designed to demonstrate core IB Computer Science SL programming constructs while providing a simple, local question bank quiz experience.

Key characteristics:

- Questions are stored in a local CSV file (`src/data/question-bank.csv`).
- The application runs entirely offline on the student’s machine.
- The student selects a topic and difficulty, answers 10 multiple-choice questions, and receives feedback and a summary.
- The implementation is intentionally small but layered for clarity (models, services, API, templates, utils).

## High-Level Architecture

The application uses a classic layered structure:

- **Models (`src/models/`)**
  - Domain data structures representing questions and quiz sessions.
- **Services (`src/services/`)**
  - Core business logic: loading the question bank, managing quiz sessions, computing summaries.
- **API (`src/api/`)**
  - FastAPI routes that coordinate between HTTP requests, services, and templates.
- **Web (`src/web/`)**
  - Jinja2 templates and static assets (CSS, JS) for the user interface.
- **Utils (`src/utils/`)**
  - Shared utilities such as timing helpers.
- **Tests (`tests/`)**
  - Unit tests for quiz logic and summaries.

### ASCII Architecture Diagram

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

The entrypoint `src/main.py` creates the FastAPI application, mounts static files, and includes the router from `src/api/routes.py`.

## Data Flow

1. **Question bank loading**
   - On first use, `src/services/quiz_service.py` reads `src/data/question-bank.csv` into memory.
   - The CSV schema is mapped into `MCQQuestion` objects from `src/models/question.py`.
   - A simple in-memory cache avoids re-reading the CSV for every request.

2. **Listing topics and difficulties**
   - The home route (`GET /`) calls service helpers to derive the set of available topics and difficulty levels from the loaded questions.
   - These sets are passed to `src/web/templates/quiz.html` for the selection dropdowns.

3. **Starting a quiz session**
   - The user submits the topic and difficulty via `POST /api/quiz/start`.
   - The service filters questions by topic and difficulty, randomly samples up to 10, and creates a `QuizSession` object with a new session ID and start time.
   - Session state is kept in an in-memory dictionary keyed by session ID.
   - The first question for the session is sent to the template and rendered as a card.

4. **Answering questions**
   - For each question, the user posts an answer to `POST /api/quiz/{session_id}/answer`.
   - The service checks correctness, records a `QuestionAttempt`, and returns the next question (if any) plus a flag indicating if the quiz is finished.
   - Per-question feedback ("Correct" / "Incorrect") is displayed above the next question.

5. **Summary and review**
   - When the final question is answered, the service records the end time and computes a summary for the session:
     - Total questions, correct and incorrect counts.
     - Percentage score.
     - Duration in seconds.
     - A list of incorrect questions with the user’s chosen answer and the correct answer.
   - The summary is displayed on the same page and is also available as JSON via `GET /api/quiz/{session_id}/summary`.

## Key Modules and Responsibilities

### Models (`src/models/question.py`)

- `BaseQuestion` and `MCQQuestion` represent quiz questions and options.
- `QuestionAttempt` captures one user answer, including correctness.
- `QuizSession` aggregates questions and attempts and exposes properties:
  - `total_questions`, `correct_count`, `incorrect_count`.
  - `score_percentage`.
  - `duration_seconds` based on `start_time` and `end_time`.

### Services (`src/services/quiz_service.py`)

- CSV handling:
  - `load_question_bank()` loads and validates the question bank from disk.
  - `get_question_bank()` exposes a cached list of questions.
- Quiz setup:
  - `get_available_topics()` and `get_available_difficulties()` derive valid filter values.
  - `create_quiz_session(topic, difficulty, num_questions)` filters questions and creates a `QuizSession` with a new UUID and a start timestamp.
- Quiz progression:
  - `get_session(session_id)` retrieves in-memory sessions.
  - `get_next_question(session_id)` selects the next question based on attempts.
  - `record_answer(session_id, question_id, chosen_option)` records a `QuestionAttempt`, determines correctness, and sets `end_time` when the quiz is finished.
- Summary:
  - `compute_quiz_summary(session_id)` builds a dictionary with totals, score, duration, and incorrect-question details for API and template consumption.

### API (`src/api/routes.py`)

- Configures Jinja2 templates and static file locations.
- `GET /`:
  - Loads topics and difficulties, handles CSV errors defensively.
  - Renders the main `quiz.html` template.
- `POST /api/quiz/start`:
  - Validates the submitted topic and difficulty.
  - Calls `create_quiz_session` and renders the first question.
- `POST /api/quiz/{session_id}/answer`:
  - Accepts a chosen option, updates the session, and either shows the next question or the finished summary.
- `GET /api/quiz/{session_id}/summary`:
  - Returns a JSON `QuizSummary` as defined in the OpenAPI contract.

### Web (`src/web/templates/` and `src/web/static/`)

- `base.html`:
  - Wraps all content with a centered container and includes the CSS and JS assets.
- `quiz.html`:
  - Renders topic and difficulty selectors at the top.
  - Shows current quiz status (topic, difficulty, “Question X of 10”).
  - Displays questions and answers in card-like sections.
  - Renders the summary and incorrect-answer review at the end of the quiz.
- `src/web/static/css/tailwind.css`:
  - A handcrafted set of Tailwind-like utility classes to style the app with a simple, dark theme.
- `src/web/static/js/htmx.min.js`:
  - Placeholder for HTMX; included so the app can be extended with partial-page updates in the future.

### Utils (`src/utils/timing.py`)

- Provides `now()` and `duration_seconds()` helpers, isolating time-related logic for easier testing and modification.

### Tests (`tests/unit/test_quiz_service.py`)

- Validate quiz service behavior:
  - Topic/difficulty derivation.
  - Session creation with proper filtering.
  - Summary totals, score percentage, incorrect-question list.
  - Non-negative duration calculations.


## Static Code Analysis Summary

*(Values below are based on simple file and line counts within this repository.)*

### Code files and lines of code

**Python files (`src/` and `tests/`):**

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

**HTML templates:**

| File                           |
|--------------------------------|
| `src/web/templates/base.html`  |
| `src/web/templates/quiz.html`  |

**Static assets:**

| Type | File                              |
|------|-----------------------------------|
| CSS  | `src/web/static/css/tailwind.css` |
| JS   | `src/web/static/js/htmx.min.js`   |

### Complexity and structure (qualitative)

- **Cyclomatic complexity**: kept deliberately low.
  - Most functions are short and single-responsibility: load data, filter collections, compute a summary, or handle a single HTTP route.
  - Control flow primarily uses simple `if` checks and list comprehensions.
- **State management**:
  - Quiz sessions are stored in a simple in-memory dictionary keyed by session ID.
  - No database or external services are used.
- **Data access pattern**:
  - The CSV question bank is read once per process and cached in memory.
  - All operations on questions (filtering, sampling) are performed on in-memory lists.
- **Testing coverage focus**:
  - Core quiz logic (session creation, answer recording, summaries) is exercised by unit tests.
  - Web templates are simple enough that they are validated primarily via manual end-to-end testing.

### Project structure summary

```text
.
├── src
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models
│   │   ├── __init__.py
│   │   └── question.py
│   ├── services
│   │   ├── __init__.py
│   │   └── quiz_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── timing.py
│   ├── web
│   │   ├── templates
│   │   │   ├── base.html
│   │   │   └── quiz.html
│   │   └── static
│   │       ├── css
│   │       │   └── tailwind.css
│   │       └── js
│   │           └── htmx.min.js
│   └── data
│       └── question-bank.csv
├── tests
│   └── unit
│       └── test_quiz_service.py
├── specs
│   └── 001-offline-quiz
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md
│       ├── contracts
│       │   └── openapi.yaml
│       └── checklists
│           └── requirements.md
└── docs
    └── architecture.md
```

This structure keeps the project small, readable, and aligned with the IB Computer Science SL goal of demonstrating core constructs without unnecessary complexity.
