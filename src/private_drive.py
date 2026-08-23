from __future__ import annotations

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
    safe = name.replace("'", "\\'")
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name,modifiedTime)",
                                 orderBy="modifiedTime desc", pageSize=10).execute().get("files", [])
    if not files:
        raise FileNotFoundError(f"Google Drive file not found: {name}")
    return _download_id(files[0]["id"], destination)


def download_recent_csvs(destination_dir: str | Path, limit: int = 20) -> list[tuple[Path, dict]]:
    """Download recent CSV-like files from the configured private Drive folder.

    This deliberately does not depend on a filename: users may keep the original
    Rakuten Securities export name. The parser decides whether each file is a
    valid Rakuten holdings export. Native Google Sheets are not considered.
    """
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


def upload_or_replace(local_path: str | Path, name: str | None = None, mime_type: str | None = None) -> str:
    from googleapiclient.http import MediaFileUpload
    service = _service(); folder = _folder_id(); p = Path(local_path)
    target = name or p.name
    safe = target.replace("'", "\\'")
    q = f"'{folder}' in parents and name='{safe}' and trashed=false"
    files = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    media = MediaFileUpload(str(p), mimetype=mime_type, resumable=False)
    if files:
        result = service.files().update(fileId=files[0]["id"], media_body=media, fields="id").execute()
    else:
        metadata = {"name": target, "parents": [folder]}
        result = service.files().create(body=metadata, media_body=media, fields="id").execute()
    return str(result["id"])
