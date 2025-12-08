from __future__ import annotations

from datetime import datetime


def now() -> datetime:
    """Return the current timestamp.

    Wrapped to keep time-related logic in one place.
    """

    return datetime.now()


def duration_seconds(start: datetime, end: datetime) -> float:
    """Return the duration between two timestamps in seconds."""

    return (end - start).total_seconds()
