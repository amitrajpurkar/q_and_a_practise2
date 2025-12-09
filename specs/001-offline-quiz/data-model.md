# Data Model: Offline Quiz Question Bank

## Overview

The data model describes how questions, quiz sessions, and individual attempts are
represented in memory after loading the CSV question bank.

## Entities

### Question (BaseQuestion / MCQQuestion)

Represents a single multiple-choice question in the question bank.

- **Fields**:
  - `id`: unique identifier for the question (e.g., integer or string key).
  - `topic`: topic/subject name (e.g., "Math", "History").
  - `difficulty`: one of `"easy"`, `"medium"`, `"hard"`.
  - `text`: the question text shown to the student.
  - `options`: ordered collection of answer options (e.g., list of 4 strings).
  - `correct_option`: identifier for the correct option (e.g., index or label such as
    "A", "B", "C", "D").

- **Relationships**:
  - Belongs to the global question bank loaded from `question-bank.csv`.
  - Referenced by many `QuestionAttempt` records and `QuizSession` objects.

- **Validation rules**:
  - `difficulty` must be one of the three allowed values.
  - `options` must contain at least two entries.
  - `correct_option` must correspond to one of the provided options.

### QuizSession

Represents one run of the quiz for a student.

- **Fields**:
  - `id`: unique identifier for the session.
  - `selected_topic`: topic chosen at quiz start.
  - `selected_difficulty`: difficulty chosen at quiz start.
  - `questions`: sequence of `Question` objects presented during the session.
  - `attempts`: sequence of `QuestionAttempt` records, in the order they were answered.
  - `start_time`: timestamp when the quiz session started.
  - `end_time`: timestamp when the quiz session ended.

- **Derived data**:
  - `total_questions`: number of questions attempted.
  - `correct_count`: number of correctly answered questions.
  - `incorrect_count`: number of incorrectly answered questions.
  - `score_percentage`: computed as `(correct_count / total_questions) * 100` when
    `total_questions > 0`.
  - `duration`: time difference between `start_time` and `end_time`.

### QuestionAttempt

Represents a student's answer to a single question within a session.

- **Fields**:
  - `question`: reference to the `Question` that was asked.
  - `chosen_option`: the option selected by the student.
  - `is_correct`: boolean flag indicating whether the chosen option matches the
    question's `correct_option`.

- **Relationships**:
  - Belongs to exactly one `QuizSession`.
  - Links a `Question` to a student's response.

## Relationships Summary

- One `QuizSession` has many `QuestionAttempt`s.
- Each `QuestionAttempt` references exactly one `Question`.
- The global question bank is a collection of `Question` objects shared across sessions.
