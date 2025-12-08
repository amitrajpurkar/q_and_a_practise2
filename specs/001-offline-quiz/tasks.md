---
description: "Task list for Offline Quiz Question Bank feature"
---

# Tasks: Offline Quiz Question Bank

**Input**: Design documents from `specs/001-offline-quiz/` (spec.md, plan.md, data-model.md, contracts/, research.md, quickstart.md)
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include file paths where applicable

## Path Conventions

- Single project: `src/` and `tests/` at repository root
- Web app layering per plan: `src/models/`, `src/services/`, `src/api/`, `src/utils/`, `src/web/`
- Data file: `src/data/question-bank.csv`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (dirs: src/, src/models/, src/services/, src/api/, src/utils/, src/web/templates/, src/web/static/css/, src/web/static/js/, src/data/, tests/unit/)
- [X] T002 Initialize uv environment for Python 3.12 and create local virtual env in project root (uv venv)
- [X] T003 [P] Install core dependencies with uv (FastAPI, uvicorn, pandas, Jinja2, pydantic) for use by modules under `src/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T004 Create domain model skeletons in `src/models/question.py` (BaseQuestion/MCQQuestion, QuizSession, QuestionAttempt classes with fields from data-model.md)
- [X] T005 [P] Implement CSV loading function in `src/services/quiz_service.py` using pandas to read `src/data/question-bank.csv` into a list of Question objects with basic validation
- [X] T006 [P] Implement timing helpers in `src/utils/timing.py` for starting/stopping timers and computing duration in seconds
- [X] T007 [P] Create FastAPI application entrypoint in `src/main.py` (app instance, template configuration, static files mount for `src/web/static`)
- [X] T008 [P] Create `src/api/routes.py` with APIRouter, route stubs for `/`, `/api/quiz/start`, `/api/quiz/{session_id}/answer`, `/api/quiz/{session_id}/summary`, and include router from `src/main.py`
- [X] T009 [P] Create base templates and static assets: `src/web/templates/base.html`, `src/web/templates/quiz.html`, `src/web/static/js/htmx.min.js`, `src/web/static/css/tailwind.css` with minimal layout and placeholders

**Checkpoint**: Application skeleton runs with uvicorn and serves a basic home page without full quiz behavior.

---

## Phase 3: User Story 1 - Take quiz by topic and difficulty (Priority: P1) 🎯 MVP

**Goal**: Allow the student to choose a topic and difficulty, start a quiz, answer questions, and track score.

**Independent Test**: From the home page, select a topic and difficulty, answer the fixed number of questions, and verify that all questions match the chosen topic and difficulty, answers are accepted, and score updates.

### Implementation for User Story 1

- [ ] T010 [US1] Implement functions in `src/services/quiz_service.py` to derive available topics and difficulties from the loaded question bank
- [ ] T011 [US1] Implement quiz session creation logic in `src/services/quiz_service.py` (filter questions by topic & difficulty, select fixed number, create QuizSession with ID and first question)
- [ ] T012 [US1] Implement `POST /api/quiz/start` handler in `src/api/routes.py` that validates topic/difficulty, calls quiz_service to create a session, and returns the first Question as JSON
- [ ] T013 [US1] Implement `GET /` handler in `src/api/routes.py` that renders `src/web/templates/quiz.html` with lists of available topics and difficulties
- [ ] T014 [P] [US1] Implement Jinja2 markup in `src/web/templates/quiz.html` to show topic/difficulty selection form and an HTMX target area for loading questions
- [ ] T015 [US1] Implement `POST /api/quiz/{session_id}/answer` handler in `src/api/routes.py` that accepts AnswerSubmission JSON, updates the QuizSession via quiz_service, and returns correctness plus next question or finished flag
- [ ] T016 [US1] Extend `src/services/quiz_service.py` with logic to record QuestionAttempt objects, update running score, and enforce fixed question count and early-exit sentinel/flags
- [ ] T017 [P] [US1] Add basic unit tests in `tests/unit/test_quiz_service.py` for topic/difficulty filtering and starting a QuizSession

**Checkpoint**: User Story 1 should be fully functional: student can choose topic & difficulty, answer a sequence of questions, and have score tracked.

---

## Phase 4: User Story 2 - View quiz summary (Priority: P2)

**Goal**: At the end of a quiz (including early exit), show a summary with totals, percentage score, and time spent.

**Independent Test**: Complete or end a quiz session and verify that the summary shows the total questions attempted, correct answers, percentage score, and duration.

### Implementation for User Story 2

- [ ] T018 [US2] Implement summary computation function in `src/services/quiz_service.py` to derive totals, percentage score, and duration from a QuizSession
- [ ] T019 [US2] Implement `GET /api/quiz/{session_id}/summary` handler in `src/api/routes.py` returning QuizSummary JSON as defined in `contracts/openapi.yaml`
- [ ] T020 [P] [US2] Update `src/web/templates/quiz.html` to fetch and render the summary (score, counts, duration) when the quiz is finished
- [ ] T021 [P] [US2] Integrate `src/utils/timing.py` with quiz lifecycle so start and end times are recorded and used in summary duration calculations

**Checkpoint**: User Story 2 should be functional: after a session ends, student can view a clear summary of performance and time spent.

---

## Phase 5: User Story 3 - Review incorrect questions (Priority: P3)

**Goal**: Show which questions were answered incorrectly along with the student’s answer and the correct answer.

**Independent Test**: Complete a quiz with at least one incorrect answer and verify that the review lists each incorrect question, the chosen option, and the correct option.

### Implementation for User Story 3

- [ ] T022 [US3] Extend summary computation in `src/services/quiz_service.py` to collect incorrect QuestionAttempt details (question, chosen_option, correct_option)
- [ ] T023 [US3] Extend `GET /api/quiz/{session_id}/summary` in `src/api/routes.py` to include incorrect question details in the QuizSummary JSON
- [ ] T024 [P] [US3] Update `src/web/templates/quiz.html` summary view to render a review section listing incorrect questions with the student’s and correct answers

**Checkpoint**: User Story 3 should be functional: summary shows a detailed review of incorrect answers when applicable and handles the “all correct” case gracefully.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, style compliance, and basic validation of flows.

- [ ] T025 [P] Run PEP8/formatting checks on all Python files under `src/` and fix any style issues
- [ ] T026 [P] Extend `tests/unit/test_quiz_service.py` with tests for summary and review calculations (totals, percentages, incorrect question list)
- [ ] T027 Perform manual end-to-end test of all user stories using steps from `specs/001-offline-quiz/quickstart.md`
- [ ] T028 [P] Validate that `uv run uvicorn src.main:app --reload` starts the app and that static assets (Tailwind CSS, HTMX) load from `src/web/static/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies – must be completed first.
- **Foundational (Phase 2)**: Depends on Setup completion – blocks all user stories.
- **User Story Phases (3–5)**: Each depends on Foundational completion.
  - User Story 1 (P1) should be implemented first as the MVP.
  - User Story 2 (P2) depends on a working quiz flow (US1).
  - User Story 3 (P3) depends on summary data structures from US2.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational – no dependencies on other stories.
- **User Story 2 (P2)**: Depends on User Story 1 (needs sessions and scoring).
- **User Story 3 (P3)**: Depends on User Story 2 (needs summary structure) and User Story 1.

### Within Each User Story

- Models and services in `src/models/` and `src/services/` before endpoints in `src/api/`.
- Endpoints before final template wiring in `src/web/templates/`.
- Summary and review logic after basic quiz flow is working.

### Parallel Opportunities

- Setup tasks T003 can run in parallel with documentation updates if any.
- Foundational tasks T005–T009 can largely run in parallel (different files).
- Within User Story 1, template work (T014) and tests (T017) can proceed in parallel with route logic once interfaces are stable.
- Within User Story 2, UI summary rendering (T020) and timing integration (T021) can proceed in parallel.
- Within User Story 3, template work (T024) can proceed in parallel with summary computation changes (T022–T023).
- Polish tasks T025, T026, and T028 can run in parallel once core functionality is in place.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL – blocks all user stories).
3. Complete Phase 3: User Story 1.
4. Stop and validate: test User Story 1 independently using the quickstart steps.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. Add User Story 1 → test independently → ready for demo (MVP).
3. Add User Story 2 → test independently → demo updated summary.
4. Add User Story 3 → test independently → demo complete review experience.

### Parallel Team Strategy (if multiple implementers)

1. One person focuses on services and data loading (`src/services/`, `src/models/`).
2. Another focuses on FastAPI routes (`src/api/`, `src/main.py`).
3. Another focuses on templates and static assets (`src/web/templates/`, `src/web/static/`).
4. All coordinate via the contracts in `specs/001-offline-quiz/contracts/openapi.yaml`.
