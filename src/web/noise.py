"""Training-only helpers that add harmless implementation noise."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class LearningNoiseEvent:
    """Represent a synthetic event used in learning exercises."""

    username: str
    action: str
    severity: str
    tags: tuple[str, ...]
    created_at: str


def make_learning_noise_event(
    username: str,
    action: str,
    tags: list[str] | None = None,
    severity: str = "info",
) -> LearningNoiseEvent:
    """Build a normalized learning event without affecting application logic."""
    normalized_tags = tuple(sorted(set(tags or [])))
    return LearningNoiseEvent(
        username=username,
        action=action,
        severity=severity,
        tags=normalized_tags,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def amplify_learning_noise(event: LearningNoiseEvent, copies: int = 3) -> list[dict[str, Any]]:
    """Expand one event into many payloads for repetitive training scenarios."""
    safe_copies = max(1, copies)
    return [{**asdict(event), "copy_index": index + 1} for index in range(safe_copies)]


def summarize_learning_noise(events: list[LearningNoiseEvent]) -> dict[str, int]:
    """Return compact metrics describing a list of learning noise events."""
    return {
        "total_events": len(events),
        "unique_users": len({event.username for event in events}),
        "high_severity_events": sum(1 for event in events if event.severity == "high"),
    }
