from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path


def _service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    raw = os.getenv("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise RuntimeError("GDRIVE_SERVICE_ACCOUNT_JSON is not set")
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _folder_id() -> str:
    folder = os.getenv("GDRIVE_FOLDER_ID", "").strip()
    if not folder:
        raise RuntimeError("GDRIVE_FOLDER_ID is not set")
    return folder


def _escape_drive_query(value: str) -> str:
    return str(value).replace("'", "\\'")


def file_sha256(local_path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(local_path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def corrected_snapshot_name(name: str, revision: int) -> str:
    p = Path(name)
    suffix = "".join(p.suffixes)
    base = p.name[:-len(suffix)] if suffix else p.name
    return f"{base}_v{revision}_corrected{suffix}"


def _download_id(file_id: str, destination: str | Path) -> Path:
    from googleapiclient.http import MediaIoBaseDownload
    service = _service()
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO(); downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    p = Path(destination); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(buf.getvalue())
    return p


def download_named(name: str, destination: str | Path) -> Path:
    service = _service(); folder = _folder_id()
    safe = _escape_drive_query(name)
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
        name = str(meta.get("name") or "")
        mime = str(meta.get("mimeType") or "")
        if mime.startswith("application/vnd.google-apps"):
            continue
        if not (name.lower().endswith((".csv", ".txt")) or "csv" in mime or mime.startswith("text/")):
            continue
        safe_name = f"{i:02d}_{Path(name).name}"
        try:
            p = _download_id(str(meta["id"]), dest / safe_name)
            out.append((p, meta))
        except Exception:
            continue
    return out


def download_recent_files(destination_dir: str | Path, limit: int = 50) -> list[tuple[Path, dict]]:
    service = _service(); folder = _folder_id()
    q = f"'{folder}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
    fields = "files(id,name,mimeType,modifiedTime,createdTime,size,md5Checksum)"
    files = service.files().list(
        q=q,
        spaces="drive",
        fields=fields,
        orderBy="modifiedTime desc",
        pageSize=max(1, min(limit, 100)),
    ).execute().get("files", [])
    out: list[tuple[Path, dict]] = []
    dest = Path(destination_dir); dest.mkdir(parents=True, exist_ok=True)
    for i, meta in enumerate(files):
        mime = str(meta.get("mimeType") or "")
        if mime.startswith("application/vnd.google-apps"):
            continue
        name = Path(str(meta.get("name") or f"drive_file_{i}")).name
        try:
            p = _download_id(str(meta["id"]), dest / f"{i:02d}_{name}")
            out.append((p, meta))
        except Exception:
            continue
    return out


def ensure_subfolder(name: str, parent_id: str | None = None) -> str:
    service = _service(); parent = parent_id or _folder_id(); safe = _escape_drive_query(name)
    q = (
        f"'{parent}' in parents and name='{safe}' and trashed=false and "
        "mimeType='application/vnd.google-apps.folder'"
    )
    files = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    if files:
        return str(files[0]["id"])
    result = service.files().create(
        body={"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]},
        fields="id",
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


def upload_or_replace(
    local_path: str | Path,
    name: str | None = None,
    mime_type: str | None = None,
    parent_id: str | None = None,
) -> str:
    from googleapiclient.http import MediaFileUpload
    service = _service(); folder = parent_id or _folder_id(); p = Path(local_path)
    target = name or p.name
    safe = _escape_drive_query(target)
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    media = MediaFileUpload(str(p), mimetype=mime_type, resumable=False)
    if files:
        result = service.files().update(fileId=files[0]["id"], media_body=media, fields="id").execute()
    else:
        metadata = {"name": target, "parents": [folder]}
        result = service.files().create(body=metadata, media_body=media, fields="id").execute()
    return str(result["id"])


def upload_immutable_snapshot(
    local_path: str | Path,
    name: str | None = None,
    mime_type: str | None = None,
    parent_id: str | None = None,
    app_properties: dict[str, str] | None = None,
) -> dict[str, str | int | bool]:
    """Persist a private historical snapshot without overwriting prior content.

    Re-running the same snapshot is idempotent when the SHA-256 is unchanged.
    If the same logical filename already exists with different content, a
    `_vN_corrected` file is created instead of mutating history.
    """
    from googleapiclient.http import MediaFileUpload
    service = _service(); folder = parent_id or _folder_id(); p = Path(local_path)
    target = name or p.name; digest = file_sha256(p)
    safe = _escape_drive_query(target)
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    fields = "files(id,name,appProperties,createdTime)"
    existing = service.files().list(q=q, spaces="drive", fields=fields, pageSize=10).execute().get("files", [])
    for item in existing:
        props = item.get("appProperties") or {}
        if props.get("sha256") == digest:
            return {"id": str(item["id"]), "name": str(item.get("name") or target), "created": False,
                    "corrected_revision": 1, "sha256": digest}

    revision = 1
    final_name = target
    if existing:
        revision = 2
        while True:
            candidate = corrected_snapshot_name(target, revision)
            safe_candidate = _escape_drive_query(candidate)
            cq = f"'{folder}' in parents and name='{safe_candidate}' and trashed=false"
            matches = service.files().list(q=cq, spaces="drive", fields=fields, pageSize=10).execute().get("files", [])
            same = next((x for x in matches if (x.get("appProperties") or {}).get("sha256") == digest), None)
            if same:
                return {"id": str(same["id"]), "name": str(same.get("name") or candidate), "created": False,
                        "corrected_revision": revision, "sha256": digest}
            if not matches:
                final_name = candidate
                break
            revision += 1
            if revision > 99:
                raise RuntimeError("too many corrected snapshot revisions")

    props = {"sha256": digest, "immutable": "true"}
    for k, v in (app_properties or {}).items():
        if v is not None:
            props[str(k)[:124]] = str(v)[:124]
    media = MediaFileUpload(str(p), mimetype=mime_type, resumable=False)
    result = service.files().create(
        body={"name": final_name, "parents": [folder], "appProperties": props},
        media_body=media,
        fields="id,name",
    ).execute()
    return {"id": str(result["id"]), "name": str(result.get("name") or final_name), "created": True,
            "corrected_revision": revision, "sha256": digest}
