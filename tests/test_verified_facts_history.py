import pytest

from verified_facts_ledger import (
    FactConflict, append_verified_fact, read_verified_facts, read_verified_history,
)


def test_new_verified_observation_retains_previous_value(tmp_path):
    path = tmp_path / "private.jsonl"
    original = append_verified_fact(
        path, key="bank:balance", value=100, scope="bank",
        observed_at="2099-01-01T10:00:00+09:00",
        evidence_ref="private:synthetic-day-one",
    )
    latest = append_verified_fact(
        path, key="bank:balance", value=120, scope="bank",
        observed_at="2099-01-02T10:00:00+09:00",
        evidence_ref="private:synthetic-day-two",
        supersedes=original["fact_id"],
    )
    history = read_verified_history(path, key="bank:balance")
    assert [row["value"] for row in history] == [100, 120]
    assert history[1]["supersedes"] == history[0]["fact_id"]
    assert read_verified_facts(path)["bank:balance"]["fact_id"] == latest["fact_id"]


def test_history_filter_still_checks_other_asset_integrity(tmp_path):
    path = tmp_path / "private.jsonl"
    append_verified_fact(path, key="bank:balance", value=100, scope="bank",
                         observed_at="2099-01-01T10:00:00+09:00",
                         evidence_ref="private:synthetic-bank")
    append_verified_fact(path, key="crypto:quantity", value=0.1, scope="crypto",
                         observed_at="2099-01-01T10:00:00+09:00",
                         evidence_ref="private:synthetic-crypto")
    lines = path.read_text().splitlines()
    lines[1] = lines[1].replace('"value":0.1', '"value":0.2')
    path.write_text("\n".join(lines) + "\n")
    with pytest.raises(FactConflict, match="integrity"):
        read_verified_history(path, key="bank:balance")


def test_missing_history_is_empty_not_zero(tmp_path):
    assert read_verified_history(tmp_path / "absent.jsonl") == []
