"""Training-only timeline helpers for synthetic noise events."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web.noise import LearningNoiseEvent


@dataclass(frozen=True)
class NoiseTimelineEntry:
    """Represent one event in timeline form."""

    username: str
    action: str
    severity: str
    timestamp: datetime
    minute_bucket: str
    is_high: bool


@dataclass(frozen=True)
class NoiseTimeline:
    """Store normalized timeline entries and timeline aggregates."""

    entries: tuple[NoiseTimelineEntry, ...]
    total_entries: int
    high_entries: int
    unique_minutes: int


def _parse_iso_timestamp(value: str) -> datetime:
    """Parse an ISO-8601 timestamp into a ``datetime`` instance."""
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _minute_bucket(timestamp: datetime) -> str:
    """Build minute precision bucket for timeline grouping."""
    return timestamp.strftime("%Y-%m-%dT%H:%M")


def build_timeline_entry(event: LearningNoiseEvent) -> NoiseTimelineEntry:
    """Convert one event into a timeline entry."""
    timestamp = _parse_iso_timestamp(event.created_at)
    return NoiseTimelineEntry(
        username=event.username,
        action=event.action,
        severity=event.severity,
        timestamp=timestamp,
        minute_bucket=_minute_bucket(timestamp),
        is_high=event.severity.lower() in {"high", "critical"},
    )


def build_noise_timeline(events: Iterable[LearningNoiseEvent]) -> NoiseTimeline:
    """Create a sorted timeline from an event sequence."""
    entries = sorted((build_timeline_entry(event) for event in events), key=lambda entry: entry.timestamp)
    return NoiseTimeline(
        entries=tuple(entries),
        total_entries=len(entries),
        high_entries=sum(1 for entry in entries if entry.is_high),
        unique_minutes=len({entry.minute_bucket for entry in entries}),
    )


def compress_timeline(timeline: NoiseTimeline, include_actions: bool = False) -> tuple[dict[str, object], ...]:
    """Summarize timeline entries by user and minute bucket."""
    grouped: dict[tuple[str, str], list[NoiseTimelineEntry]] = {}
    for entry in timeline.entries:
        key = (entry.username, entry.minute_bucket)
        grouped.setdefault(key, []).append(entry)

    rows: list[dict[str, object]] = []
    for (username, minute_bucket), entries in sorted(grouped.items()):
        row: dict[str, object] = {
            "username": username,
            "minute_bucket": minute_bucket,
            "event_count": len(entries),
            "high_count": sum(1 for entry in entries if entry.is_high),
        }
        if include_actions:
            row["actions"] = tuple(sorted({entry.action for entry in entries}))
        rows.append(row)
    return tuple(rows)


def timeline_heatmap(timeline: NoiseTimeline) -> dict[str, dict[str, int]]:
    """Return nested counts organized by user and minute bucket."""
    heatmap: dict[str, dict[str, int]] = {}
    for entry in timeline.entries:
        heatmap.setdefault(entry.username, {})
        heatmap[entry.username][entry.minute_bucket] = heatmap[entry.username].get(entry.minute_bucket, 0) + 1
    return heatmap


def detect_noise_bursts(timeline: NoiseTimeline, minimum_events: int = 3) -> tuple[str, ...]:
    """Detect user-minute buckets crossing the configured event threshold."""
    bursts = [
        f'{row["username"]}:{row["minute_bucket"]}'
        for row in compress_timeline(timeline)
        if int(row["event_count"]) >= minimum_events
    ]
    return tuple(bursts)
