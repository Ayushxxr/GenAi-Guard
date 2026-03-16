from fastapi import APIRouter, UploadFile, File
import os
import shutil

from .engine import scan_uploaded_file

router = APIRouter()

UPLOAD_DIR = "temp_uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/scan")
async def scan_file(upload_file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)

    # save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # run malware scan
    result = scan_uploaded_file(file_path)

    return {
        "status": "success",
        "result": result
    }