import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4
from dotenv import load_dotenv
import shutil

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
ALLOWED_EXT = {"doc", "docx", "pdf"}
MAX_BYTES = 1 * 1024 * 1024 # 1MB

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile, max_bytes=MAX_BYTES) -> str:
    filename = upload_file.filename
    if not filename or "." not in filename:
        raise HTTPException(status_code=400, detail="Arquivo sem nome ou sem extensão")
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Extensão '{ext}' não permitida")

    content = await upload_file.read()
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo de 1MB")

    safe_name = f"{uuid4().hex}.{ext}"
    dest_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(dest_path, "wb") as f:
        f.write(content)

    return dest_path