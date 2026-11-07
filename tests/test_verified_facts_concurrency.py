"""Concurrency regression tests use synthetic values only."""
import multiprocessing
import pytest

from verified_facts_ledger import FactConflict, append_verified_fact, read_verified_facts, read_verified_history


def _write(path, value, queue):
    try:
        append_verified_fact(path, key="cash", value=value, scope="bank",
                             observed_at="2099-01-01T10:00:00+09:00",
                             evidence_ref="private:synthetic")
        queue.put("ok")
    except FactConflict:
        queue.put("conflict")
    except Exception as exc:
        queue.put(type(exc).__name__)


def test_concurrent_conflicting_writers_cannot_both_commit(tmp_path):
    path = str(tmp_path / "facts.jsonl")
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    processes = [ctx.Process(target=_write, args=(path, value, queue))
                 for value in (100, 200)]
    for process in processes:
        process.start()
    for process in processes:
        process.join(timeout=15)
        if process.is_alive():
            process.terminate()
            process.join()
            pytest.fail("Writer blocked indefinitely")
        assert process.exitcode == 0
    assert sorted([queue.get(timeout=5), queue.get(timeout=5)]) == ["conflict", "ok"]
    history = read_verified_history(path)
    assert len(history) == 1
    assert read_verified_facts(path)["cash"]["value"] in (100, 200)


def test_lock_file_is_private(tmp_path):
    path = tmp_path / "facts.jsonl"
    append_verified_fact(path, key="cash", value=100, scope="bank",
                         observed_at="2099-01-01T10:00:00+09:00",
                         evidence_ref="private:synthetic")
    assert (path.parent / "facts.jsonl.lock").stat().st_mode & 0o777 == 0o600
