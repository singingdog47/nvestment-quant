from __future__ import annotations
import json, os
from pathlib import Path

def publish_directory(local_dir="data/intelligence"):
    raw=os.getenv("GDRIVE_SERVICE_ACCOUNT_JSON","") or os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON","")
    folder=os.getenv("GDRIVE_FOLDER_ID","") or os.getenv("GOOGLE_DRIVE_FOLDER_ID","")
    if not raw or not folder: return {"status":"skipped","reason":"Drive secrets not set"}
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        info=json.loads(raw)
        creds=Credentials.from_service_account_info(info,scopes=["https://www.googleapis.com/auth/drive.file"])
        svc=build("drive","v3",credentials=creds,cache_discovery=False)
        uploaded=[]
        for p in Path(local_dir).glob("*"):
            if not p.is_file(): continue
            q=f"name='{p.name.replace(chr(39), chr(92)+chr(39))}' and '{folder}' in parents and trashed=false"
            res=svc.files().list(q=q,fields="files(id,name)").execute().get("files",[])
            media=MediaFileUpload(str(p),resumable=False)
            if res: svc.files().update(fileId=res[0]["id"],media_body=media).execute()
            else: svc.files().create(body={"name":p.name,"parents":[folder]},media_body=media,fields="id").execute()
            uploaded.append(p.name)
        return {"status":"ok","uploaded":uploaded}
    except Exception as e:
        return {"status":"error","reason":f"{type(e).__name__}: {e}"}
