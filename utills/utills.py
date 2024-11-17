import uuid
import os
from fastapi import UploadFile
import math
import re
from typing import Annotated
from fastapi import Depends
from database.database import get_session, UploadFiles, DownloadFiles
from database.schema import File
from sqlmodel import Session
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
EXPIRED_AT = int(os.getenv("EXPIRED_AT"))
ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4", "heic", "heif"]
ALLOWED_TYPE = ["image", "video", "application"]

database = Annotated[Session, Depends(get_session)]


# Valid file extention
def ValidateExtention(file_name: str) -> tuple[bool, str]:
    ext_list = file_name.lower().split(".")
    idx = len(ext_list) - 1
    if ext_list[idx] in ALLOWED_EXT:
        return (True, ext_list[idx])
    else:
        return (False, "")


# Confirm content type
def ValidateType(content_type: str) -> tuple[bool, str]:
    type_re = re.compile(r'(^[a-z]+)/')
    type_match = type_re.search(content_type)
    type_s = type_match.group(1)

    if type_s in ALLOWED_TYPE:
        return (True, type_s)
    else:
        return (False, "")


# Add uploaded files to the database
def registerUploadFile(file: File, db: Session):
    f = UploadFiles(
        name=file.name,
        uploaded=file.uploaded,
        expired=file.expired
    )

    db.add(f)
    db.commit()
    db.refresh(f)


# Add downloaded files to the database
def registerDownloadFile(file: File, db: Session):
    f = DownloadFiles(
        name=file.name,
        uploaded=file.uploaded,
        expired=file.expired
    )

    db.add(f)
    db.commit()
    db.refresh(f)


# Saves a file to disk
async def saveFile(file: UploadFile, db: database) -> tuple[str, str]:
    _, file_ext = ValidateExtention(file.filename)
    file_id = uuid.uuid4()
    original_filename = file.filename
    file.filename = f"{file_id}.{file_ext}"
    r_file = await file.read()

    with open(f"{UPLOAD_DIR}/{file.filename}", "wb") as f:
        f.write(r_file)

    uploaded_time = datetime.now()
    expiring_time = datetime.now() + timedelta(hours=EXPIRED_AT)

    upload_file = File(
        name=file.filename,
        uploaded=uploaded_time.strftime("%Y-%m-%d %H:%M"),
        expired=expiring_time.strftime("%Y-%m-%d %H:%M")
    )

    registerUploadFile(upload_file, db)

    return (file.filename, original_filename)


# Reduce file height and width
def compressSize(file_size: tuple[int, int], quality: int) -> tuple[int, int]:
    compress_percentage = quality / 100

    width = math.floor(file_size[0] * compress_percentage)
    height = math.floor(file_size[1] * compress_percentage)

    # (Width, Height)
    return (width, height)


# Change display file name
def changeDisplayFileName(file_name: str, ext: str) -> str:
    file_list = file_name.split('.')
    new_display_name = f"{file_list[0]}.{ext}"
    return new_display_name


# Validate file size
def ValidateSize(file_size: int) -> bool:
    g_bytes = 1_073_741_824
    if file_size > g_bytes:
        return False
    else:
        return True
