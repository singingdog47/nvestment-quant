"""Private source provenance checks; never publish source bytes or their digest.

The digest is stored only in the private ledger evidence reference. The
caller must supply the actual private file; self-reported hashes are rejected.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def source_sha256(path: str | Path) -> str:
    source = Path(path)
    if not source.is_file() or source.is_symlink():
        raise ValueError("Source must be a regular non-symlink file")
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verified_source_evidence(path: str | Path, *, expected_sha256: str | None = None) -> str:
    actual = source_sha256(path)
    if expected_sha256 is not None and actual != expected_sha256.lower():
        raise ValueError("Private source file digest mismatch")
    # Avoid including the potentially sensitive original filename in the ledger.
    return "private:sha256:" + actual
