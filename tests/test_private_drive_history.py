from pathlib import Path

from private_drive import corrected_snapshot_name, file_sha256


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
