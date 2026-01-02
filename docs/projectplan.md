# Project Plan (IB Computer Science IA)

## Project context

This project is an **offline web-based quiz application** built with **Python + FastAPI + Jinja2** and a **CSV question bank**.

**Project roles:** Single developer (the student). The student assumes all responsibilities normally split across a team:

- Client communication / requirements gathering
- Analysis and design
- Implementation
- Testing and quality assurance
- Documentation and evaluation

## Planning assumptions

- Timeline is planned as a short IA project (single developer, small scope).
- Dates below are *planned* and can be adjusted as work progresses.
- Working days are assumed to be after school / evenings and weekends.

---

## SDLC task list (tabular)

### 1) Planning & initiation

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Planning | Define project goals & success criteria | 2026-01-03 | 2026-01-03 | Define what the quiz app must do (topic/difficulty selection, 10 MCQs, feedback, summary). |
| Planning | Identify stakeholders & user needs | 2026-01-03 | 2026-01-04 | Identify primary user (student) and collect needs via interview/questions. |
| Planning | Define scope, constraints, and risks | 2026-01-04 | 2026-01-04 | Set offline-only constraint, CSV data source, small feature set; list risks (data quality, time, tooling). |

### 2) Analysis (requirements)

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Analysis | Write functional requirements | 2026-01-05 | 2026-01-05 | Document functions: start quiz, answer questions, feedback, summary, review incorrect answers. |
| Analysis | Write non-functional requirements | 2026-01-05 | 2026-01-06 | Define usability, performance (local), reliability, offline operation, maintainability. |
| Analysis | Define acceptance criteria | 2026-01-06 | 2026-01-06 | Convert requirements into testable pass/fail statements. |

### 3) Design

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Design | Choose architecture & tech stack | 2026-01-07 | 2026-01-07 | Decide on FastAPI routes + service layer + models + templates + CSV input. |
| Design | Design data model (CSV → objects) | 2026-01-07 | 2026-01-08 | Define question structure, session structure, attempts, summary fields. |
| Design | Design UI navigation and page layouts | 2026-01-08 | 2026-01-09 | Design single-page flow: selection → question loop → summary/review. |
| Design | Create diagrams (flowchart, use cases, DFD) | 2026-01-09 | 2026-01-10 | Produce IA design diagrams and ensure they match implementation plan. |

### 4) Implementation

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Implementation | Set up project structure and dependencies | 2026-01-11 | 2026-01-11 | Organize folders (`src/api`, `src/services`, `src/models`, `src/web`, `src/data`). |
| Implementation | Implement CSV loading + validation | 2026-01-11 | 2026-01-12 | Read question bank CSV, validate difficulty/answers, map to question objects, cache questions. |
| Implementation | Implement quiz session creation | 2026-01-12 | 2026-01-12 | Filter by topic/difficulty, sample up to 10 questions, create UUID session, store in memory. |
| Implementation | Implement answering + progression | 2026-01-13 | 2026-01-13 | Record attempts, check correctness, move to next question, stop at end. |
| Implementation | Implement summary computation | 2026-01-13 | 2026-01-14 | Compute totals, score percentage, duration, and incorrect answer review list. |
| Implementation | Implement UI templates (Jinja2) | 2026-01-14 | 2026-01-15 | Build `base.html` and `quiz.html` forms and display logic for quiz and summary. |
| Implementation | Implement FastAPI routes | 2026-01-15 | 2026-01-16 | Implement `GET /`, `POST /api/quiz/start`, `POST /api/quiz/{session_id}/answer`, JSON summary route. |
| Implementation | Styling and usability improvements | 2026-01-16 | 2026-01-17 | Improve layout, readability, and feedback messaging using static CSS. |

### 5) Testing & quality assurance

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Testing | Create unit tests for service layer | 2026-01-18 | 2026-01-19 | Test filtering, sampling, answer recording, summary totals, and timing is non-negative. |
| Testing | Manual UI testing (functional) | 2026-01-19 | 2026-01-20 | Follow step-by-step test plan for selectors, answering, feedback, summary. |
| Testing | Negative/error-path tests | 2026-01-20 | 2026-01-20 | Test missing CSV, invalid CSV values, invalid session id, and no available questions. |
| Testing | Fix defects and re-test | 2026-01-21 | 2026-01-22 | Address issues found and rerun regression checklist. |

### 6) Documentation & IA deliverables

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Documentation | Write architecture documentation | 2026-01-23 | 2026-01-23 | Summarize layers, responsibilities, and data flow. |
| Documentation | Write design documentation | 2026-01-23 | 2026-01-24 | Document user flow, diagrams, and data model for IA Criterion C. |
| Documentation | Write test plan + record evidence | 2026-01-24 | 2026-01-25 | Produce test plan and capture evidence (screenshots/outputs) for IA. |
| Documentation | Reflection and evaluation | 2026-01-26 | 2026-01-26 | Evaluate success criteria, discuss limitations, and propose future improvements. |

### 7) Release / handover

| SDLC Phase | Task name | Planned start | Planned end | Short description |
|-----------|-----------|---------------|-------------|------------------|
| Release | Prepare offline run instructions | 2026-01-27 | 2026-01-27 | Write clear steps to run locally (install deps, start server, open browser). |
| Release | Final demo walkthrough | 2026-01-27 | 2026-01-28 | Run through end-to-end scenario and confirm acceptance criteria. |
| Release | Final submission packaging | 2026-01-28 | 2026-01-28 | Ensure repository is clean and IA documentation is complete and organized. |

---

## Milestones (summary)

| Milestone | Target date | Definition of done |
|----------|-------------|-------------------|
| Requirements complete | 2026-01-06 | Functional + non-functional requirements and acceptance criteria written. |
| Design complete | 2026-01-10 | Diagrams and data model defined and agreed with requirements. |
| Feature complete | 2026-01-17 | End-to-end quiz flow works with UI + summary. |
| Testing complete | 2026-01-22 | Unit + manual tests executed; defects fixed; regression run. |
| IA documentation complete | 2026-01-26 | Architecture, design, and testing evidence compiled. |
| Final submission | 2026-01-28 | Final run instructions + complete deliverables. |
