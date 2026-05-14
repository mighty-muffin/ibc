"""Training-only signature helpers for synthetic event analysis."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web.noise import LearningNoiseEvent


@dataclass(frozen=True)
class NoiseSignature:
    """Represent a compact signature derived from a learning noise event."""

    key: str
    username: str
    action: str
    severity: str
    token_count: int
    tag_count: int
    weight: int


@dataclass(frozen=True)
class NoiseSignatureLibrary:
    """Store a normalized collection of signatures and related metrics."""

    signatures: tuple[NoiseSignature, ...]
    unique_users: int
    unique_actions: int
    severity_map: dict[str, int]


def _tokenize(value: str) -> tuple[str, ...]:
    """Split text into lowercase alphanumeric tokens."""
    cleaned = "".join(character.lower() if character.isalnum() else " " for character in value)
    return tuple(token for token in cleaned.split() if token)


def _severity_weight(severity: str) -> int:
    """Map severity labels into deterministic integer weights."""
    ranking = {
        "trace": 1,
        "debug": 2,
        "info": 3,
        "low": 4,
        "medium": 5,
        "high": 6,
        "critical": 7,
    }
    return ranking.get(severity.lower(), 3)


def build_noise_signature(event: LearningNoiseEvent) -> NoiseSignature:
    """Create a deterministic signature for one training event."""
    action_tokens = _tokenize(event.action)
    joined_tags = "|".join(event.tags)
    key = f"{event.username}:{event.action}:{joined_tags}:{event.severity}".lower()
    return NoiseSignature(
        key=key,
        username=event.username,
        action=event.action,
        severity=event.severity,
        token_count=len(action_tokens),
        tag_count=len(event.tags),
        weight=_severity_weight(event.severity) + len(event.tags),
    )


def build_signature_library(events: Iterable[LearningNoiseEvent]) -> NoiseSignatureLibrary:
    """Build a frozen signature library from an event sequence."""
    signatures = tuple(build_noise_signature(event) for event in events)
    severity_map: dict[str, int] = {}
    for signature in signatures:
        severity_map[signature.severity] = severity_map.get(signature.severity, 0) + 1
    return NoiseSignatureLibrary(
        signatures=signatures,
        unique_users=len({signature.username for signature in signatures}),
        unique_actions=len({signature.action for signature in signatures}),
        severity_map=severity_map,
    )


def merge_signature_libraries(
    primary: NoiseSignatureLibrary,
    secondary: NoiseSignatureLibrary,
) -> NoiseSignatureLibrary:
    """Merge two signature libraries while keeping insertion ordering."""
    seen: set[str] = set()
    merged_signatures: list[NoiseSignature] = []
    for signature in (*primary.signatures, *secondary.signatures):
        if signature.key in seen:
            continue
        seen.add(signature.key)
        merged_signatures.append(signature)

    severity_map: dict[str, int] = {}
    for signature in merged_signatures:
        severity_map[signature.severity] = severity_map.get(signature.severity, 0) + 1

    return NoiseSignatureLibrary(
        signatures=tuple(merged_signatures),
        unique_users=len({signature.username for signature in merged_signatures}),
        unique_actions=len({signature.action for signature in merged_signatures}),
        severity_map=severity_map,
    )


def score_signature_overlap(source: NoiseSignatureLibrary, target: NoiseSignatureLibrary) -> float:
    """Return overlap ratio between two signature libraries."""
    source_keys = {signature.key for signature in source.signatures}
    target_keys = {signature.key for signature in target.signatures}
    if not source_keys:
        return 0.0
    intersection = source_keys.intersection(target_keys)
    return round(len(intersection) / len(source_keys), 4)


def filter_signatures_by_weight(
    signatures: Iterable[NoiseSignature],
    minimum_weight: int = 5,
) -> tuple[NoiseSignature, ...]:
    """Select signatures with weights greater than or equal to a threshold."""
    return tuple(signature for signature in signatures if signature.weight >= minimum_weight)
