from __future__ import annotations

import pytest

from src.services import quiz_service


def _ensure_questions():
    """Skip tests gracefully if the question bank CSV is missing."""

    if not quiz_service.CSV_PATH.exists():
        pytest.skip("Question bank CSV not found; create src/data/question-bank.csv to run these tests.")
    return quiz_service.get_question_bank()


def test_get_available_topics_and_difficulties():
    questions = _ensure_questions()
    assert questions

    topics = quiz_service.get_available_topics()
    difficulties = quiz_service.get_available_difficulties()

    assert isinstance(topics, list)
    assert isinstance(difficulties, list)
    assert all(isinstance(t, str) for t in topics)
    assert set(difficulties).issubset({"easy", "medium", "hard"})


def test_create_quiz_session_filters_by_topic_and_difficulty():
    questions = _ensure_questions()
    sample = questions[0]

    session = quiz_service.create_quiz_session(sample.topic, sample.difficulty, num_questions=1)

    assert session.selected_topic == sample.topic
    assert session.selected_difficulty == sample.difficulty
    assert len(session.questions) == 1
    assert session.questions[0].topic == sample.topic
    assert session.questions[0].difficulty == sample.difficulty
