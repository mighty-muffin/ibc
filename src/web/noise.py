"""Training-only helpers that add harmless implementation noise."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from web.noise_payloads import (
    estimate_payload_entropy,
    flatten_payload_matrix,
    materialize_payload_matrix,
    payload_size_distribution,
)
from web.noise_signatures import (
    build_signature_library,
    filter_signatures_by_weight,
)
from web.noise_timeline import (
    build_noise_timeline,
    compress_timeline,
    detect_noise_bursts,
    timeline_heatmap,
)


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


def build_learning_noise_matrix(
    usernames: list[str],
    actions: list[str],
    severities: list[str] | None = None,
) -> tuple[LearningNoiseEvent, ...]:
    """Create a subtle Cartesian matrix of synthetic events for exercises."""
    selected_severities = severities or ["info"]
    events: list[LearningNoiseEvent] = []
    for username in usernames:
        for action in actions:
            for severity in selected_severities:
                tags = [f"user:{username}", f"action:{action}", f"severity:{severity}"]
                events.append(
                    make_learning_noise_event(
                        username=username,
                        action=action,
                        tags=tags,
                        severity=severity,
                    )
                )
    return tuple(events)


def summarize_learning_noise_bundle(events: list[LearningNoiseEvent]) -> dict[str, Any]:
    """Build richer summaries while keeping all logic training-only."""
    timeline = build_noise_timeline(events)
    signature_library = build_signature_library(events)
    weighted_signatures = filter_signatures_by_weight(signature_library.signatures, minimum_weight=6)
    payload_matrix = materialize_payload_matrix(events)
    flattened_payloads = flatten_payload_matrix(payload_matrix)

    return {
        "event_summary": summarize_learning_noise(events),
        "timeline_summary": {
            "total_entries": timeline.total_entries,
            "high_entries": timeline.high_entries,
            "unique_minutes": timeline.unique_minutes,
            "bursts": detect_noise_bursts(timeline, minimum_events=2),
            "heatmap": timeline_heatmap(timeline),
            "compressed": compress_timeline(timeline, include_actions=True),
        },
        "signature_summary": {
            "total_signatures": len(signature_library.signatures),
            "unique_users": signature_library.unique_users,
            "unique_actions": signature_library.unique_actions,
            "severity_map": signature_library.severity_map,
            "weighted_signatures": tuple(signature.key for signature in weighted_signatures),
        },
        "payload_summary": {
            "rows": len(payload_matrix),
            "distribution": payload_size_distribution(payload_matrix),
            "entropy": estimate_payload_entropy(payload_matrix),
            "preview": flattened_payloads[:3],
        },
    }
