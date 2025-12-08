# Implementation Plan: Offline Quiz Question Bank

**Branch**: `001-offline-quiz` | **Date**: 2025-12-08 | **Spec**: specs/001-offline-quiz/spec.md
**Input**: Feature specification from `/specs/001-offline-quiz/spec.md`

**Note**: This plan is generated for the `/speckit.plan` workflow and must respect the
Q and A Practise 2 constitution (minimal files, IB CS SL focus, PEP8 compliance, and
coverage of required Python constructs).

## Summary

Implement an offline quiz web application that reads a predefined multiple-choice
question bank from a local CSV file, allows the student to choose a topic and
difficulty (easy/medium/hard), delivers a fixed-length quiz session, and then shows a
summary with score, time spent, and a review of incorrect answers. The application will
be built in Python 3.12 using uv (Astral) as the package manager, FastAPI for the
backend, pandas to load and map the CSV into `Question` objects, and a simple Jinja2
web UI enhanced by HTMX and Tailwind CSS. The project structure is intentionally
lightweight but layered (models, services, api, utils, web) to remain easy to read for
IB Computer Science SL assessment while still demonstrating object-oriented design and
other required constructs.

## Technical Context

**Language/Version**: Python 3.12 (CPython)  
**Primary Dependencies**: FastAPI, uvicorn, pandas, Jinja2, pydantic, uv (Astral) as
package manager, HTMX (served as local static JS), Tailwind CSS (served as local static
CSS)  
**Storage**: Local CSV file (`src/data/question-bank.csv`) loaded into memory via pandas
at application startup; no external database or remote services.  
**Testing**: pytest for basic unit tests on quiz logic and manual testing of the web UI
flows (start quiz, answer questions, view summary).  
**Target Platform**: Local desktop/laptop running Python 3.12 in a uv-managed
environment; FastAPI app served via uvicorn for local browser access.  
**Project Type**: web  
**Performance Goals**: Single-user offline usage with sub-second responses for loading
questions and rendering summaries for a question bank up to a few thousand rows.  
**Constraints**: Offline-capable (no network calls or external databases at runtime);
minimal file count and simple structure per IB CS SL constitution; all Python code must
be PEP8-compliant.  
**Scale/Scope**: Single user at a time; question bank size on the order of hundreds to a
few thousand questions; no horizontal scaling requirements.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Minimal Files & Simplicity (P1)**:
  - Plan uses a single FastAPI application with a small number of Python modules:
    - `src/main.py`
    - `src/models/question.py`
    - `src/services/quiz_service.py`
    - `src/api/routes.py`
    - `src/utils/timing.py`
  - Web layer adds only essential templates (`base.html`, `quiz.html`) and static
    assets (`tailwind.css`, `htmx.min.js`).
  - No extra packages, microservices, or subprojects are introduced. This is considered
    acceptable within the constitution as a minimal structure that still demonstrates
    separation of concerns.

- **IB Computer Science SL Alignment (P2)**:
  - Feature demonstrates core IB concepts: arrays/lists, records/objects, selection,
    iteration, OOP design, and file I/O over a CSV question bank.
  - Web UI and endpoints remain simple and focused on the quiz scenario so that code is
    easy for IB CS SL students and examiners to read.

- **Core Python Construct Coverage (P3)** — this feature contributes:
  - Arrays/lists for the in-memory question bank and session attempts.
  - User-defined objects / data records: `Question`, `QuizSession`, `QuestionAttempt`.
  - Simple and complex selection in quiz flow (topic/difficulty filtering, correctness
    checks, early exit).
  - Loops and nested loops when filtering questions and iterating through attempts.
  - User-defined methods with parameters and return values inside service and model
    classes.
  - Sorting/searching across question collections where needed (for example, by
    topic/difficulty or identifier).
  - File I/O and parsing via pandas loading `question-bank.csv` and mapping rows to
    domain objects.
  - Sentinels/flags to control quiz loop termination and early-exit behavior.
  - Recursion in at least one helper in `quiz_service.py` (for example, recursively
    processing attempts when building a summary) chosen explicitly to satisfy IB
    requirements.
  - Merging of sorted data structures (for example, merging per-difficulty question
    lists when constructing a combined view or review order).
  - Inheritance, polymorphism, and encapsulation via a small class hierarchy
    (for example, `BaseQuestion` and `MCQQuestion`) and encapsulated service classes.

- **PEP8-Compliant Style (P4)**:
  - All Python modules will follow PEP8 naming and layout.
  - Plan will include tasks to run a formatter/linter or perform manual PEP8 checks
    before submission.

- **Learnability & Transparency (P5)**:
  - Modules are named by responsibility (`models`, `services`, `api`, `utils`, `web`).
  - Each required construct (for example, recursion, inheritance) will be placed in
    clearly named functions or classes and referenced in documentation so IB examiners
    can easily locate them.

*Gate result*: **PASS**, assuming we keep to the small, explicitly listed set of modules
and templates. Any additional modules/files beyond this list must be justified in
Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-offline-quiz/
├── plan.md         # This file (/speckit.plan command output)
├── research.md     # Phase 0 output (/speckit.plan)
├── data-model.md   # Phase 1 output (/speckit.plan)
├── quickstart.md   # Phase 1 output (/speckit.plan)
├── contracts/      # Phase 1 output (/speckit.plan)
└── tasks.md        # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── main.py                  # FastAPI app factory and routing include
├── models/
│   └── question.py          # Question, BaseQuestion/MCQQuestion, QuizSession, QuestionAttempt
├── services/
│   └── quiz_service.py      # Quiz logic: load CSV via pandas, selection, scoring, recursion, merging
├── api/
│   └── routes.py            # FastAPI endpoints for quiz flow (start, answer, summary)
├── utils/
│   └── timing.py            # Timing helpers, sentinels/flags, utility functions
└── web/
    ├── templates/
    │   ├── base.html        # Shared layout with Tailwind + HTMX includes
    │   └── quiz.html        # Quiz page and partials
    └── static/
        ├── css/
        │   └── tailwind.css # Pre-built Tailwind CSS (local, no CDN)
        └── js/
            └── htmx.min.js  # Local HTMX script (no CDN)

src/data/
└── question-bank.csv        # Local question bank (topic, difficulty, text, options, correct option)

tests/
└── unit/
    └── test_quiz_service.py # Optional simple unit tests for quiz logic
```

**Structure Decision**: Single web project under `src/` with light layering into
`models`, `services`, `api`, `utils`, and `web` to support clarity and IB OOP
demonstrations while keeping the total number of Python and template files minimal.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|---------------------------------------|
| Additional modules beyond a single `main.py` | Clarify separation of concerns (domain model, quiz logic, API, utilities) and make IB constructs (inheritance, polymorphism, encapsulation) explicit | Single monolithic file would be harder for IB examiners to read and would obscure individual constructs; small set of modules still satisfies "minimal but clear" principle |
