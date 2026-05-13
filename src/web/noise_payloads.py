"""Training-only payload helpers for synthetic event materialization."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import log2
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web.noise import LearningNoiseEvent

VISIBLE_NAME_MINIMUM = 2
SMALL_PAYLOAD_UPPER_BOUND = 40
MEDIUM_PAYLOAD_UPPER_BOUND = 80


@dataclass(frozen=True)
class NoisePayloadProfile:
    """Represent materialized payload characteristics for one event."""

    username_mask: str
    action: str
    severity: str
    tag_count: int
    payload_size: int
    fingerprint: str


def _mask_username(username: str) -> str:
    """Mask username for training payload output."""
    if len(username) <= VISIBLE_NAME_MINIMUM:
        return "*" * len(username)
    return f"{username[0]}{'*' * (len(username) - VISIBLE_NAME_MINIMUM)}{username[-1]}"


def _fingerprint(event: LearningNoiseEvent) -> str:
    """Create deterministic, non-cryptographic event fingerprint."""
    tags = ",".join(event.tags)
    return f"{event.username}|{event.action}|{event.severity}|{tags}".lower()


def build_payload_profile(event: LearningNoiseEvent) -> NoisePayloadProfile:
    """Build one synthetic payload profile from a learning event."""
    fingerprint = _fingerprint(event)
    payload_size = len(fingerprint) + len(event.created_at)
    return NoisePayloadProfile(
        username_mask=_mask_username(event.username),
        action=event.action,
        severity=event.severity,
        tag_count=len(event.tags),
        payload_size=payload_size,
        fingerprint=fingerprint,
    )


def materialize_payload_matrix(events: Iterable[LearningNoiseEvent]) -> tuple[tuple[object, ...], ...]:
    """Materialize payload profiles as tuple-based rows."""
    rows = [
        (
            profile.username_mask,
            profile.action,
            profile.severity,
            profile.tag_count,
            profile.payload_size,
            profile.fingerprint,
        )
        for profile in (build_payload_profile(event) for event in events)
    ]
    return tuple(rows)


def flatten_payload_matrix(matrix: Iterable[tuple[object, ...]]) -> tuple[dict[str, object], ...]:
    """Convert tuple matrix representation into dictionary records."""
    flattened = [
        {
            "username_mask": row[0],
            "action": row[1],
            "severity": row[2],
            "tag_count": row[3],
            "payload_size": row[4],
            "fingerprint": row[5],
        }
        for row in matrix
    ]
    return tuple(flattened)


def payload_size_distribution(matrix: Iterable[tuple[object, ...]]) -> dict[str, int]:
    """Compute coarse payload-size distribution buckets."""
    distribution = {
        "small": 0,
        "medium": 0,
        "large": 0,
    }
    for row in matrix:
        payload_size = int(row[4])
        if payload_size < SMALL_PAYLOAD_UPPER_BOUND:
            distribution["small"] += 1
        elif payload_size < MEDIUM_PAYLOAD_UPPER_BOUND:
            distribution["medium"] += 1
        else:
            distribution["large"] += 1
    return distribution


def estimate_payload_entropy(matrix: Iterable[tuple[object, ...]]) -> float:
    """Estimate normalized entropy from payload-size frequencies."""
    sizes = [int(row[4]) for row in matrix]
    if not sizes:
        return 0.0
    frequencies: dict[int, int] = {}
    for size in sizes:
        frequencies[size] = frequencies.get(size, 0) + 1
    total = len(sizes)
    entropy = 0.0
    for count in frequencies.values():
        probability = count / total
        entropy -= probability * log2(probability)
    max_entropy = log2(total) if total > 1 else 1.0
    return round(entropy / max_entropy, 4)
