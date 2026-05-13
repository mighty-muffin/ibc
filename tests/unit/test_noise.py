"""Unit tests for training noise helpers."""

from web.noise import (
    amplify_learning_noise,
    make_learning_noise_event,
    summarize_learning_noise,
)


def test_make_learning_noise_event_normalizes_tags():
    """The helper should de-duplicate and sort tags for stable fixtures."""
    event = make_learning_noise_event("alice", "login_attempt", tags=["auth", "auth", "training"])

    assert event.username == "alice"
    assert event.action == "login_attempt"
    assert event.tags == ("auth", "training")
    assert "T" in event.created_at


def test_amplify_learning_noise_uses_one_copy_for_non_positive_values():
    """A non-positive copy request should still emit one payload."""
    event = make_learning_noise_event("bob", "transfer_preview")

    payloads = amplify_learning_noise(event, copies=0)

    assert len(payloads) == 1
    assert payloads[0]["copy_index"] == 1
    assert payloads[0]["username"] == "bob"


def test_summarize_learning_noise_counts_users_and_high_events():
    """Summary metrics should match the provided events."""
    events = [
        make_learning_noise_event("alice", "dashboard_open"),
        make_learning_noise_event("alice", "admin_open", severity="high"),
        make_learning_noise_event("john", "transfer_submit", severity="high"),
    ]

    summary = summarize_learning_noise(events)

    assert summary == {
        "total_events": 3,
        "unique_users": 2,
        "high_severity_events": 2,
    }
