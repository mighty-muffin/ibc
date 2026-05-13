"""Unit tests for training noise timeline helpers."""

from web.noise import make_learning_noise_event
from web.noise_timeline import (
    build_noise_timeline,
    compress_timeline,
    detect_noise_bursts,
    timeline_heatmap,
)

TOTAL_EVENTS = 3
HIGH_EVENTS = 2
MIN_COMPRESSED_ROWS = 2


def test_build_noise_timeline_tracks_high_and_minute_counts():
    """Timeline aggregates should reflect the input events."""
    events = [
        make_learning_noise_event("alice", "dashboard_open", severity="info"),
        make_learning_noise_event("alice", "transfer_submit", severity="high"),
        make_learning_noise_event("john", "login_attempt", severity="critical"),
    ]

    timeline = build_noise_timeline(events)

    assert timeline.total_entries == TOTAL_EVENTS
    assert timeline.high_entries == HIGH_EVENTS
    assert timeline.unique_minutes >= 1
    assert timeline.entries[0].timestamp <= timeline.entries[-1].timestamp


def test_compress_timeline_and_heatmap_output():
    """Timeline compression and heatmap data should be internally consistent."""
    events = [
        make_learning_noise_event("alice", "dashboard_open", severity="info"),
        make_learning_noise_event("alice", "transfer_submit", severity="high"),
        make_learning_noise_event("john", "login_attempt", severity="info"),
    ]

    timeline = build_noise_timeline(events)
    compressed = compress_timeline(timeline, include_actions=True)
    heatmap = timeline_heatmap(timeline)

    assert len(compressed) >= MIN_COMPRESSED_ROWS
    assert "actions" in compressed[0]
    assert isinstance(compressed[0]["actions"], tuple)
    assert heatmap["alice"]
    assert sum(sum(user_counts.values()) for user_counts in heatmap.values()) == timeline.total_entries


def test_detect_noise_bursts_with_minimum_threshold():
    """Burst detection should use grouped event count thresholds."""
    events = [make_learning_noise_event("alice", "transfer_submit", severity="high") for _ in range(4)]
    timeline = build_noise_timeline(events)

    bursts = detect_noise_bursts(timeline, minimum_events=3)

    assert len(bursts) == 1
    assert bursts[0].startswith("alice:")
