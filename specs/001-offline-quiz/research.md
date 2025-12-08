# Research: Offline Quiz Question Bank

## Decision: Language, runtime, and package manager

- **Decision**: Use Python 3.12 (CPython) with uv (Astral) as the package manager.
- **Rationale**: Python 3.12 is current, well-supported, and matches IB CS SL emphasis on
  Python. uv provides fast, reproducible dependency management in a single-tool
  workflow, keeping setup simple for a small project.
- **Alternatives considered**: Python 3.10/3.11 with pip/venv, Poetry. These are viable
  but add either slightly older runtimes or more configuration overhead without clear
  benefit for this small offline app.

## Decision: Web framework and runtime

- **Decision**: Use FastAPI with uvicorn for the local web backend.
- **Rationale**: FastAPI provides a simple, modern way to define HTTP endpoints and
  integrates well with Pydantic data models and Jinja2 templates. It keeps the codebase
  explicit and readable for IB CS SL while supporting a clean separation between API
  logic and presentation.
- **Alternatives considered**: Flask (simpler but less structured), Django (more
  batteries-included but heavier and more modular than needed), pure CLI app (would not
  satisfy the explicit requirement for a web UI).

## Decision: CSV loading and data handling

- **Decision**: Use pandas to load `src/data/question-bank.csv` and map rows into
  `Question`/`MCQQuestion` objects.
- **Rationale**: pandas provides robust CSV parsing and data manipulation, reducing the
  amount of manual parsing code while still allowing clear demonstration of file I/O and
  conversion from tabular data to user-defined objects.
- **Alternatives considered**: Python built-in `csv` module (lighter, but requires more
  parsing code and manual error handling). Given the IB requirement to keep code clear
  but also show data handling, pandas is a good balance.

## Decision: Templating and frontend behavior

- **Decision**: Use Jinja2 templates served by FastAPI, enhanced with HTMX for partial
  page updates and Tailwind CSS for styling, all served from local static files.
- **Rationale**: Jinja2 is straightforward for server-side rendering and aligns with
  IB-level understanding of templates. HTMX enables incremental updates (e.g., loading
  next question) without building a full SPA. Tailwind CSS keeps styling expressive
  without large CSS files, and pre-built CSS can be stored locally to maintain offline
  behavior.
- **Alternatives considered**: Plain HTML without HTMX (simpler but less interactive);
  full SPA with React/Vue (more complex and outside IB CS SL scope); CDN-hosted assets
  (would break the offline requirement).

## Decision: Data model design

- **Decision**: Represent domain concepts with a small set of classes: `BaseQuestion`,
  `MCQQuestion`, `QuizSession`, and `QuestionAttempt`.
- **Rationale**: This supports IB-required OOP concepts (inheritance, polymorphism,
  encapsulation) while keeping the model small and focused. Question bank rows map
  directly into these records, and the session entity captures attempts and scoring.
- **Alternatives considered**: Using plain dictionaries or tuples only (simpler but does
  not highlight OOP constructs clearly); a more complex hierarchy of question types
  (unnecessary for this feature).

## Decision: Use of recursion and merging of sorted structures

- **Decision**: Implement at least one recursive helper in `quiz_service.py` (for
  example, recursively aggregating statistics over a list of `QuestionAttempt`s) and a
  merge function that combines two or more sorted lists of questions into a single
  sorted list.
- **Rationale**: These patterns are not strictly required by the problem but are
  explicitly required by the project constitution for IB CS SL demonstration. Implement
  them in a small, well-documented way within the service layer so they are easy to
  locate and explain.
- **Alternatives considered**: Purely iterative implementations (simpler but would not
  demonstrate recursion or merging of sorted data structures).

## Decision: Testing strategy

- **Decision**: Use pytest for a small set of unit tests focusing on quiz logic
  (question selection, scoring, summary calculation) and rely on manual UI testing for
  the web flow.
- **Rationale**: A few targeted tests help validate core logic without introducing a
  large testing framework footprint. Manual testing via the browser is sufficient for
  this small offline app.
- **Alternatives considered**: No automated tests (simpler but less robust), full
  integration and UI testing (more complete but disproportionate to project size).
