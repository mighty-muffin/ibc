"""Training-only helpers that add harmless implementation noise."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class LearningNoiseEvent:
    """
    Represent a synthetic event used in learning exercises.

    Attributes:
        username: Account name associated with the practice event.
        action: Human-readable action label (for example, ``login_attempt``).
        severity: Free-form level used by exercises (for example, ``info`` or ``high``).
        tags: Sorted unique training labels tied to the event.
        created_at: ISO-8601 timestamp for when the event payload was created.
    """

    username: str
    action: str
    severity: str
    tags: tuple[str, ...]
    created_at: str


def _normalize_tags(tags: list[str] | None) -> tuple[str, ...]:
    """Normalize tags into a sorted and deduplicated tuple."""
    return tuple(sorted(set(tags or [])))


def make_learning_noise_event(
    username: str,
    action: str,
    tags: list[str] | None = None,
    severity: str = "info",
) -> LearningNoiseEvent:
    """Build a normalized learning event without affecting application logic."""
    return LearningNoiseEvent(
        username=username,
        action=action,
        severity=severity,
        tags=_normalize_tags(tags),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def amplify_learning_noise(event: LearningNoiseEvent, copy_count: int = 3) -> list[dict[str, Any]]:
    """
    Expand one event into many payloads for repetitive training scenarios.

    When ``copy_count`` is zero or negative, the function still returns one payload.
    Each returned dictionary includes all ``LearningNoiseEvent`` fields plus
    a one-based ``copy_index`` key.
    """
    normalized_copy_count = max(1, copy_count)
    return [{**asdict(event), "copy_index": index + 1} for index in range(normalized_copy_count)]


def summarize_learning_noise(events: list[LearningNoiseEvent]) -> dict[str, int]:
    """
    Return compact metrics describing a list of learning noise events.

    The result includes ``total_events``, ``unique_users``, and
    ``high_severity_events``.
    """
    return {
        "total_events": len(events),
        "unique_users": len({event.username for event in events}),
        "high_severity_events": sum(1 for event in events if event.severity == "high"),
    }
