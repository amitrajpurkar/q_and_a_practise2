# Quickstart: Offline Quiz Question Bank

## Prerequisites

- Python 3.12 installed on your machine.
- `uv` (Astral) installed for dependency and environment management.
- This repository cloned locally.

## 1. Create and activate the environment

From the repository root:

```bash
uv venv
source .venv/bin/activate  # or equivalent on your platform
```

## 2. Install dependencies

```bash
uv pip install fastapi uvicorn pandas jinja2 pydantic
```

(HTMX and Tailwind CSS will be included as local static files in `src/web/static/` and
do not require separate Python packages.)

## 3. Prepare the question bank CSV

Create the file `src/data/question-bank.csv` with a header row that matches the
`Question`/`MCQQuestion` model fields, for example:

```csv
id,topic,difficulty,text,option_a,option_b,option_c,option_d,correct_option
1,Math,easy,"What is 2+2?",2,3,4,5,C
2,History,medium,"In which year did X happen?",1914,1918,1939,1945,B
```

- `difficulty` must be one of `easy`, `medium`, or `hard`.
- `correct_option` should identify the correct choice (for example, `A`, `B`, `C`, or
  `D`).

## 4. Run the application

From the repository root, after dependencies are installed and the CSV is in place:

```bash
uv run uvicorn src.main:app --reload
```

- This starts the FastAPI app locally (by default on `http://127.0.0.1:8000`).
- Open the URL in a browser to access the quiz UI.

## 5. Use the application

1. On the home page, choose a topic and difficulty (easy/medium/hard).
2. Start the quiz to receive the first question.
3. Answer each question; the system tracks your score and progress.
4. You may end the quiz early; the system will still show a partial summary and review.
5. At the end, view the summary with total questions, correct answers, percentage
   score, time spent, and a list of questions you answered incorrectly with the correct
   answers.

## 6. Notes

- The app is designed to work entirely offline after dependencies are installed
  (question data is loaded from the local CSV file, and static assets are served
  locally).
- All Python code should follow PEP8 guidelines.
