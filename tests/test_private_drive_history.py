from pathlib import Path

from private_drive import (
    _is_generated_private_output,
    canonical_json_sha256,
    corrected_snapshot_name,
    encode_json_cell,
    file_sha256,
    history_revision,
)


def test_corrected_snapshot_name_preserves_suffix():
    assert corrected_snapshot_name("valuation_snapshot_20260831.json", 2) == "valuation_snapshot_20260831_v2_corrected.json"
    assert corrected_snapshot_name("portfolio_snapshot_20260831.csv", 7) == "portfolio_snapshot_20260831_v7_corrected.csv"


def test_corrected_snapshot_name_handles_multi_suffix():
    assert corrected_snapshot_name("snapshot.json.gz", 3) == "snapshot_v3_corrected.json.gz"


def test_file_sha256_is_stable(tmp_path: Path):
    p = tmp_path / "x.json"
    p.write_text('{"a":1}\n', encoding="utf-8")
    first = file_sha256(p)
    second = file_sha256(p)
    assert first == second
    assert len(first) == 64


def test_file_sha256_changes_when_content_changes(tmp_path: Path):
    p = tmp_path / "x.json"
    p.write_text("one", encoding="utf-8")
    first = file_sha256(p)
    p.write_text("two", encoding="utf-8")
    assert file_sha256(p) != first


def test_generated_private_outputs_are_excluded_from_input_scan():
    assert _is_generated_private_output("portfolio_latest.csv")
    assert _is_generated_private_output("portfolio_valuation_latest.json")
    assert not _is_generated_private_output("保有商品一覧_20260831_160400.csv")


def test_canonical_hash_ignores_run_timestamp_but_not_metrics():
    a = {"generated_at": "2026-09-01T01:00:00Z", "metrics": {"pe": 15.0}}
    b = {"generated_at": "2026-09-01T02:00:00Z", "metrics": {"pe": 15.0}}
    c = {"generated_at": "2026-09-01T02:00:00Z", "metrics": {"pe": 16.0}}
    assert canonical_json_sha256(a) == canonical_json_sha256(b)
    assert canonical_json_sha256(a) != canonical_json_sha256(c)


def test_history_revision_is_idempotent_for_same_hash():
    digest = "a" * 64
    rows = [["2026-08-31", "valuation", 1, False, digest]]
    assert history_revision(rows, "2026-08-31", "valuation", digest) == {
        "skip": True, "revision": 1, "is_corrected": False
    }


def test_history_revision_appends_correction_for_changed_hash():
    rows = [
        ["2026-08-31", "valuation", 1, False, "a" * 64],
        ["2026-08-31", "valuation", 2, True, "b" * 64],
    ]
    state = history_revision(rows, "2026-08-31", "valuation", "c" * 64)
    assert state == {"skip": False, "revision": 3, "is_corrected": True}


def test_encode_json_cell_compresses_large_payload_without_truncation():
    text = encode_json_cell({"payload": "x" * 60000})
    assert "gzip+base64" in text
    assert len(text) < 48000
