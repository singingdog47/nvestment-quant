"""Independent 5m Challenger1 fork; original 1m ledger is never written."""
from __future__ import annotations

import json
from pathlib import Path

import shadow_challenger2 as fork_engine

DATA_ROOT = Path("data")
OUT_DIR = DATA_ROOT / "shadow_challenger1_5m"
CONFIG_FILE = Path("config/shadow_challenger1_5m_v1.json")


def run(as_of=None, bar_source=None):
    previous = (fork_engine.DATA_ROOT, fork_engine.OUT_DIR, fork_engine.CONFIG_FILE)
    try:
        fork_engine.DATA_ROOT = DATA_ROOT
        fork_engine.OUT_DIR = OUT_DIR
        fork_engine.CONFIG_FILE = CONFIG_FILE
        return fork_engine.run(as_of=as_of, bar_source=bar_source)
    finally:
        fork_engine.DATA_ROOT, fork_engine.OUT_DIR, fork_engine.CONFIG_FILE = previous


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
