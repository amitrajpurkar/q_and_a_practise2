from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class BaseQuestion:
    """Base question fields shared by all question types."""

    id: str
    topic: str
    difficulty: str
    text: str


@dataclass
class MCQQuestion(BaseQuestion):
    """Multiple-choice question with options and a single correct answer."""

    options: List[str]
    correct_option: str


@dataclass
class QuestionAttempt:
    """One attempt by the student to answer a question."""

    question: MCQQuestion
    chosen_option: str
    is_correct: bool


@dataclass
class QuizSession:
    """Represents one quiz run for a student."""

    id: str
    selected_topic: str
    selected_difficulty: str
    questions: List[MCQQuestion] = field(default_factory=list)
    attempts: List[QuestionAttempt] = field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def total_questions(self) -> int:
        return len(self.attempts)

    @property
    def correct_count(self) -> int:
        return sum(1 for attempt in self.attempts if attempt.is_correct)

    @property
    def incorrect_count(self) -> int:
        return self.total_questions - self.correct_count

    @property
    def score_percentage(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return (self.correct_count / self.total_questions) * 100.0

    @property
    def duration_seconds(self) -> float:
        if not self.start_time or not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()
