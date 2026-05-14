"""Unit tests for training noise payload helpers."""

from web.noise import make_learning_noise_event
from web.noise_payloads import (
    build_payload_profile,
    estimate_payload_entropy,
    flatten_payload_matrix,
    materialize_payload_matrix,
    payload_size_distribution,
)

TAG_COUNT = 2
MATRIX_ROWS = 2
DISTRIBUTION_TOTAL = 3


def test_build_payload_profile_masks_username_and_generates_fingerprint():
    """Payload profiles should mask usernames and keep deterministic fingerprints."""
    event = make_learning_noise_event("alice", "transfer_submit", tags=["ops", "risk"], severity="high")

    profile = build_payload_profile(event)

    assert profile.username_mask == "a***e"
    assert profile.tag_count == TAG_COUNT
    assert profile.payload_size > 0
    assert "alice|transfer_submit|high|ops,risk" in profile.fingerprint


def test_materialize_and_flatten_payload_matrix():
    """Tuple and dictionary payload representations should stay aligned."""
    events = [
        make_learning_noise_event("alice", "dashboard_open", tags=["training"]),
        make_learning_noise_event("john", "login_attempt", tags=["auth"], severity="low"),
    ]

    matrix = materialize_payload_matrix(events)
    flattened = flatten_payload_matrix(matrix)

    assert len(matrix) == MATRIX_ROWS
    assert len(flattened) == MATRIX_ROWS
    assert flattened[0]["username_mask"] == "a***e"
    assert flattened[1]["action"] == "login_attempt"
    assert flattened[1]["severity"] == "low"


def test_payload_distribution_and_entropy():
    """Distribution and entropy helpers should return bounded values."""
    events = [
        make_learning_noise_event("a", "x", tags=["t"]),
        make_learning_noise_event("alice", "dashboard_open", tags=["training"]),
        make_learning_noise_event("john", "transfer_submit", tags=["risk", "ops"], severity="high"),
    ]
    matrix = materialize_payload_matrix(events)

    distribution = payload_size_distribution(matrix)
    entropy = estimate_payload_entropy(matrix)

    assert sum(distribution.values()) == DISTRIBUTION_TOTAL
    assert 0.0 <= entropy <= 1.0
