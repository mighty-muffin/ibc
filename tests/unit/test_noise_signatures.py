"""Unit tests for training noise signature helpers."""

from web.noise import make_learning_noise_event
from web.noise_signatures import (
    build_noise_signature,
    build_signature_library,
    filter_signatures_by_weight,
    merge_signature_libraries,
    score_signature_overlap,
)

PAIR_COUNT = 2
HEAVY_WEIGHT_MINIMUM = 6
EXPECTED_OVERLAP = 0.5


def test_build_noise_signature_uses_event_fields():
    """Signatures should include deterministic field-derived values."""
    event = make_learning_noise_event(
        "alice",
        "Transfer Submit",
        tags=["training", "auth"],
        severity="high",
    )

    signature = build_noise_signature(event)

    assert signature.username == "alice"
    assert signature.action == "Transfer Submit"
    assert signature.tag_count == PAIR_COUNT
    assert signature.token_count == PAIR_COUNT
    assert signature.weight >= HEAVY_WEIGHT_MINIMUM
    assert signature.key.startswith("alice:transfer submit")


def test_build_signature_library_and_merge_behavior():
    """Libraries should keep unique signature keys when merged."""
    event_one = make_learning_noise_event("alice", "dashboard_open", tags=["training"], severity="info")
    event_two = make_learning_noise_event("john", "transfer_submit", tags=["risk"], severity="high")
    event_three = make_learning_noise_event("alice", "dashboard_open", tags=["training"], severity="info")

    first_library = build_signature_library([event_one, event_two])
    second_library = build_signature_library([event_three])
    merged = merge_signature_libraries(first_library, second_library)

    assert first_library.unique_users == PAIR_COUNT
    assert first_library.unique_actions == PAIR_COUNT
    assert merged.unique_users == PAIR_COUNT
    assert len(merged.signatures) == PAIR_COUNT
    assert merged.severity_map["info"] == 1
    assert merged.severity_map["high"] == 1


def test_filter_and_overlap_for_signature_libraries():
    """Weight filtering and overlap scoring should be stable."""
    baseline = [
        make_learning_noise_event("alice", "dashboard_open", tags=["training"], severity="info"),
        make_learning_noise_event("john", "transfer_submit", tags=["risk", "ops"], severity="high"),
    ]
    candidate = [
        baseline[1],
        make_learning_noise_event("sarah", "login_attempt", tags=["auth"], severity="low"),
    ]

    base_library = build_signature_library(baseline)
    candidate_library = build_signature_library(candidate)
    heavy_signatures = filter_signatures_by_weight(base_library.signatures, minimum_weight=6)
    overlap = score_signature_overlap(base_library, candidate_library)

    assert len(heavy_signatures) == 1
    assert heavy_signatures[0].username == "john"
    assert overlap == EXPECTED_OVERLAP
