from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from src.models.question import MCQQuestion


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "question-bank.csv"


def load_question_bank() -> List[MCQQuestion]:
    """Load questions from the CSV into MCQQuestion objects.

    Expected CSV columns (at minimum):
    id, topic, difficulty, text, option_a, option_b, option_c, option_d, correct_option
    """

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Question bank CSV not found at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    required_columns = {
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

    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in question bank CSV: {missing}")

    questions: List[MCQQuestion] = []
    for _, row in df.iterrows():
        difficulty = str(row["difficulty"]).strip().lower()
        if difficulty not in {"easy", "medium", "hard"}:
            # Skip or raise depending on strictness; here we choose to raise.
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

    return questions
