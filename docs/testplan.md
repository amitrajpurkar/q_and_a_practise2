# Test Plan (IB Computer Science IA)

## Purpose

This test plan provides step-by-step tests for verifying each feature of the **Offline Quiz Application**.

**System under test:**

- FastAPI application with Jinja2 UI
- CSV-backed question bank (`src/data/question-bank.csv`)

**Key routes/features:**

- `GET /` (home page + selectors)
- `POST /api/quiz/start` (create quiz session)
- `POST /api/quiz/{session_id}/answer` (answer questions)
- `GET /api/quiz/{session_id}/summary` (JSON summary)

## Test environment

- OS: macOS
- Browser: any modern browser (Safari / Chrome / Firefox)
- Python environment configured to run the FastAPI app
- CSV file present at `src/data/question-bank.csv`

## Pre-test checklist

- Ensure the app starts without errors.
- Ensure `src/data/question-bank.csv` exists.
- Confirm the CSV contains at least:
  - One `topic`
  - Difficulties including `easy`, `medium`, `hard` (case-insensitive is accepted; service normalizes to lowercase)

## Test data notes

The service supports two schemas:

- **Schema v2 (current CSV):** `topic`, `question`, `option1-4`, `answer`, `difficulty` (required)
- **Schema v1 (alternative):** `id`, `topic`, `difficulty`, `text`, `option_a-d`, `correct_option` (required)

For most tests, use the repository’s existing CSV as-is.

---

## Manual functional tests (UI)

### TC-UI-01: Home page loads and shows selectors

- **Feature:** Home page renders and loads topics/difficulties from CSV
- **Steps:**
  1. Start the application.
  2. Open the browser and navigate to `http://127.0.0.1:<port>/` (or the port you configured).
  3. Observe the page header and the form.
- **Expected result:**
  - Page title “Offline Quiz” is visible.
  - Topic dropdown is visible.
  - Difficulty dropdown is visible.
  - “Start quiz” button is visible.
  - No error message is shown (unless CSV is missing/broken).

### TC-UI-02: Topic dropdown is populated from CSV

- **Feature:** Topic list derived from `MCQQuestion.topic`
- **Steps:**
  1. On `GET /`, open the Topic dropdown.
  2. Verify there are items (e.g., Physics/Chemistry/Math depending on CSV).
- **Expected result:**
  - Dropdown contains topics from the CSV.
  - Topics are sorted.

### TC-UI-03: Difficulty dropdown is populated and formatted

- **Feature:** Difficulties derived from CSV and displayed capitalized in UI
- **Steps:**
  1. On `GET /`, open the Difficulty dropdown.
  2. Verify available values.
- **Expected result:**
  - Dropdown contains `Easy`, `Medium`, `Hard` (capitalized presentation).

### TC-UI-04: Required validation prevents starting without selections

- **Feature:** Browser-side required validation on form inputs
- **Steps:**
  1. On `GET /`, do not select a topic.
  2. Do not select a difficulty.
  3. Click “Start quiz”.
- **Expected result:**
  - Browser prevents submission and highlights missing required fields.

### TC-UI-05: Start quiz creates a session and displays Question 1

- **Feature:** `POST /api/quiz/start` creates session + shows first question
- **Steps:**
  1. Select a valid Topic.
  2. Select a valid Difficulty.
  3. Click “Start quiz”.
- **Expected result:**
  - A question card appears.
  - The question text is visible.
  - Four radio options are visible.
  - The page shows “Quiz in progress for <topic> – <difficulty> (Question 1 of Y)”.
  - `Y` is `len(session.questions)` (up to 10).

### TC-UI-06: Required validation prevents submitting without choosing an option

- **Feature:** Required radio selection on answer form
- **Steps:**
  1. Start a quiz.
  2. Without selecting any answer option, click “Submit answer”.
- **Expected result:**
  - Browser prevents submission and indicates a required selection.

### TC-UI-07: Submitting an answer shows immediate feedback

- **Feature:** Correct/incorrect feedback after `POST /api/quiz/{session_id}/answer`
- **Steps:**
  1. Start a quiz.
  2. Select any option.
  3. Click “Submit answer”.
- **Expected result:**
  - A feedback message appears near the top of the quiz region:
    - “Correct!” if chosen matches the correct option.
    - “Incorrect.” otherwise.
  - The next question is displayed (unless it was the last question).

### TC-UI-08: Quiz progresses through all questions

- **Feature:** Session progression based on `len(session.attempts)`
- **Steps:**
  1. Start a quiz.
  2. Answer questions repeatedly until the quiz ends.
- **Expected result:**
  - Question index increments by 1 each time.
  - After the last question, question card disappears and summary appears.

### TC-UI-09: Summary appears when quiz is finished

- **Feature:** Summary is computed and rendered at completion
- **Steps:**
  1. Complete a quiz by answering all questions.
- **Expected result:**
  - “Quiz summary” section appears.
  - It shows:
    - Questions attempted (`summary.total_questions`)
    - Correct answers (`summary.correct_count`)
    - Incorrect answers (`summary.incorrect_count`)
    - Score percentage
    - Time spent (seconds)

### TC-UI-10: Incorrect-answer review list appears when there are mistakes

- **Feature:** Review list shows incorrect questions + chosen/correct
- **Steps:**
  1. Start a quiz.
  2. Intentionally answer at least one question incorrectly.
  3. Finish the quiz.
- **Expected result:**
  - “Review incorrect answers” appears.
  - Each listed item shows:
    - Question text
    - Your answer
    - Correct answer

### TC-UI-11: Perfect score shows the “All answers were correct” message

- **Feature:** Alternate UI summary branch when no incorrect answers
- **Steps:**
  1. Start a quiz.
  2. Answer every question correctly.
  3. Finish the quiz.
- **Expected result:**
  - Instead of a list, a message appears:
    - “All answers were correct – great job!”

---

## API / integration tests (manual using browser or curl)

### TC-API-01: Summary endpoint returns JSON

- **Feature:** `GET /api/quiz/{session_id}/summary`
- **Steps:**
  1. Start a quiz via the UI.
  2. Copy the `session_id` from the current page URL used for answer posts (or inspect network requests).
  3. Open in browser:
     - `http://127.0.0.1:<port>/api/quiz/<session_id>/summary`
- **Expected result:**
  - JSON is returned with keys:
    - `total_questions`, `correct_count`, `incorrect_count`, `score_percentage`, `duration_seconds`, `incorrect_questions`.

### TC-API-02: Unknown session id returns 404 for answer submit

- **Feature:** Robust handling for invalid session ids
- **Steps:**
  1. Send a POST request to:
     - `/api/quiz/not-a-real-session/answer`
  2. Include form fields `question_id` and `chosen_option`.
- **Expected result:**
  - Response status is **404**.

---

## Error-handling tests (data and validation)

### TC-ERR-01: Missing CSV file shows a load error

- **Feature:** Defensive error handling on home route
- **Steps:**
  1. Temporarily rename `src/data/question-bank.csv` (e.g., `question-bank.csv.bak`).
  2. Restart the server.
  3. Visit `GET /`.
- **Expected result:**
  - Page loads but shows a clear error message (e.g., “Question bank CSV not found…”).
  - Topic/difficulty dropdowns are empty.

### TC-ERR-02: Starting quiz for a topic/difficulty with no questions

- **Feature:** `create_quiz_session` fails gracefully when no matching questions
- **Steps:**
  1. Modify the CSV (or choose combinations) so there is no match for selected topic+difficulty.
  2. Attempt to start quiz.
- **Expected result:**
  - The page returns an error (HTTP 400) and displays:
    - “No questions available for the chosen topic and difficulty.”

### TC-ERR-03: Invalid difficulty values in CSV are rejected

- **Feature:** CSV validation in `load_question_bank()`
- **Steps:**
  1. Edit a row in the CSV so `difficulty` becomes an invalid value (e.g., `SuperHard`).
  2. Restart the server.
  3. Visit `GET /`.
- **Expected result:**
  - An error is shown and the app does not populate dropdowns.

### TC-ERR-04: Invalid answer in CSV is rejected (schema v2)

- **Feature:** CSV validation ensures `answer` is one of the options
- **Steps:**
  1. In a schema v2 row, set `answer` to a value not equal to `option1-4`.
  2. Restart the server.
  3. Visit `GET /`.
- **Expected result:**
  - Load fails with an error message about the answer not being one of the options.

---

## Non-functional tests

### TC-NF-01: Offline behaviour

- **Goal:** Confirm no internet dependency
- **Steps:**
  1. Disable Wi‑Fi.
  2. Start the app.
  3. Complete a quiz.
- **Expected result:**
  - App works normally.
  - No external requests are required for the quiz to function.

### TC-NF-02: Basic performance (local)

- **Goal:** Ensure responsiveness
- **Steps:**
  1. Start a quiz.
  2. Submit answers rapidly for 10 questions.
- **Expected result:**
  - Each page update happens quickly.
  - No timeouts or noticeable lag.

---

## Regression checklist (after changes)

After modifying the CSV schema, quiz logic, or templates, rerun at minimum:

- TC-UI-01 (home page)
- TC-UI-05 (start quiz)
- TC-UI-07 (feedback)
- TC-UI-09 (summary)
- TC-API-01 (JSON summary)

## Test log template (for IA evidence)

Use this table to record results:

| Test Case ID | Date | Tester | Result (Pass/Fail) | Notes / Evidence (screenshots, output) |
|-------------|------|--------|--------------------|----------------------------------------|
|             |      |        |                    |                                        |
