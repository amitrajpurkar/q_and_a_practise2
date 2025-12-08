from __future__ import annotations

from pathlib import Path
from typing import List, Any
import random
import uuid

import pandas as pd

from src.models.question import MCQQuestion, QuizSession, QuestionAttempt
from src.utils import timing


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "question-bank.csv"


def load_question_bank() -> List[MCQQuestion]:
    """Load questions from the CSV into MCQQuestion objects.

    Expected CSV columns (at minimum):
    id, topic, difficulty, text, option_a, option_b, option_c, option_d, correct_option
    """

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Question bank CSV not found at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    columns = set(df.columns)

    # Original documented schema
    schema_v1 = {
        "id",
        "topic",
        "difficulty",
        "text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_option",
    }

    # Schema used in the provided CSV: topic, question, option1-4, answer, difficulty, ...
    schema_v2 = {
        "topic",
        "question",
        "option1",
        "option2",
        "option3",
        "option4",
        "answer",
        "difficulty",
    }

    questions: List[MCQQuestion] = []

    if schema_v1.issubset(columns):
        for _, row in df.iterrows():
            difficulty = str(row["difficulty"]).strip().lower()
            if difficulty not in {"easy", "medium", "hard"}:
                raise ValueError(
                    f"Invalid difficulty '{difficulty}' for question id={row['id']}"
                )

            options = [
                str(row["option_a"]),
                str(row["option_b"]),
                str(row["option_c"]),
                str(row["option_d"]),
            ]

            correct = str(row["correct_option"]).strip().upper()
            if correct not in {"A", "B", "C", "D"}:
                raise ValueError(
                    f"Invalid correct_option '{correct}' for question id={row['id']}"
                )

            index_map = {"A": 0, "B": 1, "C": 2, "D": 3}
            correct_option_value = options[index_map[correct]]

            question = MCQQuestion(
                id=str(row["id"]),
                topic=str(row["topic"]),
                difficulty=difficulty,
                text=str(row["text"]),
                options=options,
                correct_option=correct_option_value,
            )
            questions.append(question)

    elif schema_v2.issubset(columns):
        for index, row in df.iterrows():
            difficulty = str(row["difficulty"]).strip().lower()
            if difficulty not in {"easy", "medium", "hard"}:
                raise ValueError(
                    f"Invalid difficulty '{difficulty}' for row index={index}"
                )

            options = [
                str(row["option1"]),
                str(row["option2"]),
                str(row["option3"]),
                str(row["option4"]),
            ]

            answer = str(row["answer"])
            if answer not in options:
                raise ValueError(
                    f"Answer '{answer}' is not one of the options for row index={index}"
                )

            question = MCQQuestion(
                id=str(index),
                topic=str(row["topic"]),
                difficulty=difficulty,
                text=str(row["question"]),
                options=options,
                correct_option=answer,
            )
            questions.append(question)

    else:
        raise ValueError(
            "Question bank CSV is missing required columns for a known schema; "
            f"found columns: {sorted(columns)}"
        )

    return questions


_QUESTIONS_CACHE: List[MCQQuestion] | None = None
_SESSIONS: dict[str, QuizSession] = {}
QUIZ_LENGTH = 5


def get_question_bank() -> List[MCQQuestion]:
    global _QUESTIONS_CACHE
    if _QUESTIONS_CACHE is None:
        _QUESTIONS_CACHE = load_question_bank()
    return _QUESTIONS_CACHE


def get_available_topics() -> List[str]:
    questions = get_question_bank()
    return sorted({q.topic for q in questions})


def get_available_difficulties() -> List[str]:
    questions = get_question_bank()
    return sorted({q.difficulty for q in questions})


def create_quiz_session(topic: str, difficulty: str, num_questions: int = QUIZ_LENGTH) -> QuizSession:
    questions = [
        q
        for q in get_question_bank()
        if q.topic == topic and q.difficulty == difficulty
    ]
    if not questions:
        raise ValueError("No questions available for the chosen topic and difficulty.")

    if len(questions) > num_questions:
        questions = random.sample(questions, num_questions)

    session_id = str(uuid.uuid4())
    session = QuizSession(
        id=session_id,
        selected_topic=topic,
        selected_difficulty=difficulty,
        questions=questions,
        start_time=timing.now(),
    )
    _SESSIONS[session_id] = session
    return session


def get_session(session_id: str) -> QuizSession:
    try:
        return _SESSIONS[session_id]
    except KeyError as exc:
        raise KeyError(f"Unknown session_id '{session_id}'") from exc


def get_next_question(session_id: str) -> MCQQuestion | None:
    session = get_session(session_id)
    index = len(session.attempts)
    if index >= len(session.questions):
        return None
    return session.questions[index]


def record_answer(
    session_id: str,
    question_id: str,
    chosen_option: str,
) -> tuple[bool, MCQQuestion | None, bool]:
    session = get_session(session_id)
    question = get_next_question(session_id)
    if question is None:
        return False, None, True

    is_correct = chosen_option == question.correct_option

    attempt = QuestionAttempt(
        question=question,
        chosen_option=chosen_option,
        is_correct=is_correct,
    )
    session.attempts.append(attempt)

    next_question = get_next_question(session_id)
    finished = next_question is None
    if finished and session.end_time is None:
        session.end_time = timing.now()
    return is_correct, next_question, finished


def compute_quiz_summary(session_id: str) -> dict[str, Any]:
    session = get_session(session_id)

    if session.start_time is None:
        session.start_time = timing.now()

    if session.end_time is None:
        session.end_time = timing.now()

    duration = timing.duration_seconds(session.start_time, session.end_time)

    return {
        "total_questions": session.total_questions,
        "correct_count": session.correct_count,
        "incorrect_count": session.incorrect_count,
        "score_percentage": session.score_percentage,
        "duration_seconds": duration,
        "incorrect_questions": [],
    }

