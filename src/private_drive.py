from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import io
import json
import math
import os
from pathlib import Path
from typing import Any

GENERATED_PRIVATE_OUTPUT_NAMES = {
    "portfolio_latest.csv",
    "portfolio_import_latest.json",
    "portfolio_risk_latest.json",
    "portfolio_risk_latest.md",
    "portfolio_alerts_latest.json",
    "portfolio_alerts_latest.md",
    "portfolio_policy_latest.json",
    "portfolio_policy_latest.md",
    "portfolio_valuation_latest.json",
    "portfolio_valuation_latest.md",
    "portfolio_monthly_latest.json",
    "portfolio_monthly_latest.md",
    "snapshot_manifest_latest.json",
}

HISTORY_LEDGER_NAME = "investment_quant_private_history_ledger.csv"
HISTORY_HEADER = [
    "snapshot_date", "snapshot_kind", "revision", "is_corrected", "sha256",
    "system_version", "source_file", "source_as_of", "status", "analysis_mode",
    "evidence_tier", "coverage_json", "payload_json", "created_at_utc",
]
VOLATILE_JSON_KEYS = {
    "generated_at", "generated_at_utc", "created_at", "created_at_utc", "run_at", "run_at_utc",
}


def _credentials():
    from google.oauth2 import service_account
    raw = os.getenv("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise RuntimeError("GDRIVE_SERVICE_ACCOUNT_JSON is not set")
    info = json.loads(raw)
    return service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"]
    )


def _service():
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=_credentials(), cache_discovery=False)


def _folder_id() -> str:
    folder = os.getenv("GDRIVE_FOLDER_ID", "").strip()
    if not folder:
        raise RuntimeError("GDRIVE_FOLDER_ID is not set")
    return folder


def _escape_drive_query(value: str) -> str:
    return str(value).replace("'", "\\'")


def _is_generated_private_output(name: str) -> bool:
    return Path(str(name)).name in GENERATED_PRIVATE_OUTPUT_NAMES


def file_sha256(local_path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(local_path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _canonicalize_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(k): _canonicalize_json(v)
            for k, v in sorted(value.items(), key=lambda item: str(item[0]))
            if str(k) not in VOLATILE_JSON_KEYS
        }
    if isinstance(value, list):
        return [_canonicalize_json(v) for v in value]
    if isinstance(value, tuple):
        return [_canonicalize_json(v) for v in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def canonical_json_sha256(value: Any) -> str:
    canonical = _canonicalize_json(value)
    raw = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def encode_json_cell(value: Any, max_chars: int = 48000) -> str:
    """Encode JSON losslessly; large payloads use gzip+base64 instead of truncation."""
    clean = _canonicalize_json(value)
    raw = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    if len(raw) <= max_chars:
        return raw
    packed = base64.b64encode(gzip.compress(raw.encode("utf-8"), compresslevel=9)).decode("ascii")
    wrapper = json.dumps(
        {"encoding": "gzip+base64", "original_chars": len(raw), "data": packed},
        ensure_ascii=False, separators=(",", ":"),
    )
    if len(wrapper) > max_chars:
        raise ValueError(f"history payload remains too large after compression: {len(wrapper)} chars")
    return wrapper


def corrected_snapshot_name(name: str, revision: int) -> str:
    p = Path(name)
    suffix = "".join(p.suffixes)
    base = p.name[:-len(suffix)] if suffix else p.name
    return f"{base}_v{revision}_corrected{suffix}"


def history_revision(existing_rows: list[list[Any]], snapshot_date: str, snapshot_kind: str, digest: str) -> dict[str, Any]:
    revisions: list[int] = []
    for row in existing_rows:
        if len(row) < 5 or str(row[0]) != snapshot_date or str(row[1]) != snapshot_kind:
            continue
        try:
            revision = int(float(row[2]))
        except (TypeError, ValueError):
            revision = 1
        revisions.append(max(1, revision))
        if str(row[4]) == digest:
            return {"skip": True, "revision": revision, "is_corrected": revision > 1}
    revision = max(revisions, default=0) + 1
    return {"skip": False, "revision": revision, "is_corrected": revision > 1}


def _download_bytes(file_id: str) -> bytes:
    from googleapiclient.http import MediaIoBaseDownload
    request = _service().files().get_media(fileId=file_id)
    buf = io.BytesIO(); downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def _download_id(file_id: str, destination: str | Path) -> Path:
    p = Path(destination); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_download_bytes(file_id))
    return p


def download_named(name: str, destination: str | Path) -> Path:
    service = _service(); folder = _folder_id(); safe = _escape_drive_query(name)
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name,modifiedTime)",
                                 orderBy="modifiedTime desc", pageSize=10).execute().get("files", [])
    if not files:
        raise FileNotFoundError(f"Google Drive file not found: {name}")
    return _download_id(files[0]["id"], destination)


def download_recent_csvs(destination_dir: str | Path, limit: int = 20) -> list[tuple[Path, dict]]:
    service = _service(); folder = _folder_id()
    q = f"'{folder}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
    fields = "files(id,name,mimeType,modifiedTime,size)"
    files = service.files().list(q=q, spaces="drive", fields=fields,
                                 orderBy="modifiedTime desc", pageSize=max(1, min(limit, 100))).execute().get("files", [])
    out: list[tuple[Path, dict]] = []
    dest = Path(destination_dir); dest.mkdir(parents=True, exist_ok=True)
    for i, meta in enumerate(files):
        name = str(meta.get("name") or ""); mime = str(meta.get("mimeType") or "")
        if mime.startswith("application/vnd.google-apps") or _is_generated_private_output(name):
            continue
        if not (name.lower().endswith((".csv", ".txt")) or "csv" in mime or mime.startswith("text/")):
            continue
        try:
            out.append((_download_id(str(meta["id"]), dest / f"{i:02d}_{Path(name).name}"), meta))
        except Exception:
            continue
    return out


def download_recent_files(destination_dir: str | Path, limit: int = 50) -> list[tuple[Path, dict]]:
    service = _service(); folder = _folder_id()
    q = f"'{folder}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
    fields = "files(id,name,mimeType,modifiedTime,createdTime,size,md5Checksum)"
    files = service.files().list(q=q, spaces="drive", fields=fields, orderBy="modifiedTime desc",
                                 pageSize=max(1, min(limit, 100))).execute().get("files", [])
    out: list[tuple[Path, dict]] = []
    dest = Path(destination_dir); dest.mkdir(parents=True, exist_ok=True)
    for i, meta in enumerate(files):
        mime = str(meta.get("mimeType") or "")
        name = Path(str(meta.get("name") or f"drive_file_{i}")).name
        if mime.startswith("application/vnd.google-apps") or _is_generated_private_output(name):
            continue
        try:
            out.append((_download_id(str(meta["id"]), dest / f"{i:02d}_{name}"), meta))
        except Exception:
            continue
    return out


def ensure_subfolder(name: str, parent_id: str | None = None) -> str:
    service = _service(); parent = parent_id or _folder_id(); safe = _escape_drive_query(name)
    q = f"'{parent}' in parents and name='{safe}' and trashed=false and mimeType='application/vnd.google-apps.folder'"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    if files:
        return str(files[0]["id"])
    result = service.files().create(
        body={"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]}, fields="id"
    ).execute()
    return str(result["id"])


def ensure_folder_path(parts: list[str], parent_id: str | None = None) -> str:
    folder = parent_id or _folder_id()
    for part in parts:
        clean = str(part).strip()
        if not clean or clean in {".", ".."} or "/" in clean:
            raise ValueError(f"invalid Drive folder path component: {part!r}")
        folder = ensure_subfolder(clean, folder)
    return folder


def find_history_ledger(name: str = HISTORY_LEDGER_NAME) -> str:
    service = _service(); folder = ensure_folder_path(["history", "portfolio"]); safe = _escape_drive_query(name)
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name,mimeType,modifiedTime)",
                                 orderBy="modifiedTime desc", pageSize=10).execute().get("files", [])
    if not files:
        raise FileNotFoundError(
            f"Private history ledger not found: {name}. Create it with a quota-owning Google user in history/portfolio."
        )
    return str(files[0]["id"])


def _parse_history_csv(raw: bytes) -> tuple[list[str], list[list[str]]]:
    text = raw.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return HISTORY_HEADER.copy(), []
    header = [str(x).strip() for x in rows[0]]
    if header != HISTORY_HEADER:
        raise ValueError(f"private history ledger header mismatch: {header}")
    return header, rows[1:]


def append_history_ledger(entries: list[dict[str, Any]], ledger_name: str = HISTORY_LEDGER_NAME) -> dict[str, Any]:
    """Append logical snapshots to one user-owned CSV file using Drive API only.

    Old logical rows are never removed or edited. Rewriting the same Drive file
    creates a provider revision while avoiding service-account file-creation quota.
    """
    if not entries:
        return {"status": "ok", "appended": 0, "idempotent": 0, "ledger_id": None, "rows": []}
    ledger_id = find_history_ledger(ledger_name)
    header, existing = _parse_history_csv(_download_bytes(ledger_id))
    append_rows: list[list[Any]] = []
    result_rows: list[dict[str, Any]] = []
    virtual_existing = [list(r) for r in existing]

    for entry in entries:
        snapshot_date = str(entry.get("snapshot_date") or "").strip()
        snapshot_kind = str(entry.get("snapshot_kind") or "").strip()
        digest = str(entry.get("sha256") or "").strip()
        if not snapshot_date or not snapshot_kind or len(digest) != 64:
            raise ValueError("history entry requires snapshot_date, snapshot_kind, and SHA-256")
        state = history_revision(virtual_existing, snapshot_date, snapshot_kind, digest)
        if state["skip"]:
            result_rows.append({"snapshot_date": snapshot_date, "snapshot_kind": snapshot_kind,
                                "revision": state["revision"], "created": False})
            continue
        revision = int(state["revision"]); corrected = bool(state["is_corrected"])
        row = [
            snapshot_date, snapshot_kind, revision, corrected, digest,
            str(entry.get("system_version") or ""), str(entry.get("source_file") or ""),
            str(entry.get("source_as_of") or ""), str(entry.get("status") or ""),
            str(entry.get("analysis_mode") or ""), str(entry.get("evidence_tier") or ""),
            str(entry.get("coverage_json") or ""), str(entry.get("payload_json") or ""),
            str(entry.get("created_at_utc") or ""),
        ]
        append_rows.append(row)
        virtual_existing.append([snapshot_date, snapshot_kind, revision, corrected, digest])
        result_rows.append({"snapshot_date": snapshot_date, "snapshot_kind": snapshot_kind,
                            "revision": revision, "created": True})

    if append_rows:
        output = io.StringIO(newline="")
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(existing)
        writer.writerows(append_rows)
        data = output.getvalue().encode("utf-8")
        from googleapiclient.http import MediaIoBaseUpload
        media = MediaIoBaseUpload(io.BytesIO(data), mimetype="text/csv", resumable=False)
        _service().files().update(fileId=ledger_id, media_body=media, fields="id,modifiedTime").execute()

    return {
        "status": "ok", "ledger_id": ledger_id, "appended": len(append_rows),
        "idempotent": len(entries) - len(append_rows), "rows": result_rows,
    }


def upload_or_replace(
    local_path: str | Path, name: str | None = None, mime_type: str | None = None, parent_id: str | None = None
) -> str:
    from googleapiclient.http import MediaFileUpload
    service = _service(); folder = parent_id or _folder_id(); p = Path(local_path); target = name or p.name
    safe = _escape_drive_query(target); q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    media = MediaFileUpload(str(p), mimetype=mime_type, resumable=False)
    if files:
        result = service.files().update(fileId=files[0]["id"], media_body=media, fields="id").execute()
    else:
        result = service.files().create(body={"name": target, "parents": [folder]}, media_body=media, fields="id").execute()
    return str(result["id"])
