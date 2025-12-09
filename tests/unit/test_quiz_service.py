from __future__ import annotations

import pytest

from src.services import quiz_service


def _ensure_questions():
    """Skip tests gracefully if the question bank CSV is missing."""

    if not quiz_service.CSV_PATH.exists():
        pytest.skip(
            "Question bank CSV not found; create src/data/question-bank.csv "
            "to run these tests."
        )
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

    session = quiz_service.create_quiz_session(
        sample.topic,
        sample.difficulty,
        num_questions=1,
    )

    assert session.selected_topic == sample.topic
    assert session.selected_difficulty == sample.difficulty
    assert len(session.questions) == 1
    assert session.questions[0].topic == sample.topic
    assert session.questions[0].difficulty == sample.difficulty


def test_compute_quiz_summary_totals_and_percentage_and_incorrect_list():
    questions = _ensure_questions()
    sample = questions[0]

    session = quiz_service.create_quiz_session(
        sample.topic,
        sample.difficulty,
        num_questions=2,
    )

    first = session.questions[0]
    second = session.questions[1]

    # First answer correct.
    quiz_service.record_answer(session.id, first.id, first.correct_option)

    # Second answer intentionally incorrect: pick an option that is not correct.
    wrong_option = next(
        opt for opt in second.options if opt != second.correct_option
    )
    quiz_service.record_answer(session.id, second.id, wrong_option)

    summary = quiz_service.compute_quiz_summary(session.id)

    assert summary["total_questions"] == 2
    assert summary["correct_count"] == 1
    assert summary["incorrect_count"] == 1
    assert summary["score_percentage"] == pytest.approx(50.0)

    incorrect = summary["incorrect_questions"]
    assert len(incorrect) == 1

    item = incorrect[0]
    assert item["chosen_option"] == wrong_option
    assert item["correct_option"] == second.correct_option
    assert item["question"]["id"] == second.id


def test_compute_quiz_summary_duration_non_negative():
    questions = _ensure_questions()
    sample = questions[0]

    session = quiz_service.create_quiz_session(
        sample.topic,
        sample.difficulty,
        num_questions=1,
    )

    question = session.questions[0]
    quiz_service.record_answer(session.id, question.id, question.correct_option)

    summary = quiz_service.compute_quiz_summary(session.id)

    assert summary["total_questions"] == 1
    assert summary["correct_count"] == 1
    assert summary["incorrect_count"] == 0
    assert summary["duration_seconds"] >= 0.0
