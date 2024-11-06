import uuid
import os
from fastapi import UploadFile

BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4"]


# Valid file extention
def ValidateExtention(file_name: str) -> tuple:
    ext_list = file_name.lower().split(".")
    idx = len(ext_list) - 1
    if ext_list[idx] in ALLOWED_EXT:
        return (True, ext_list[idx])
    else:
        return (False, "")


ALLOWED_TYPE = ["image", "video"]


# Confirm content type
def ValidateType(content_type: str) -> tuple:
    type_s = content_type[0:5].lower()
    if type_s in ALLOWED_TYPE:
        return (True, type_s)
    else:
        return (False, "")


# Saves a file to disk
async def saveFile(file: UploadFile) -> str:
    _, file_ext = ValidateExtention(file.filename)
    file_id = uuid.uuid4()
    file.filename = f"{file_id}.{file_ext}"
    r_file = await file.read()

    with open(f"{UPLOAD_DIR}/{file.filename}", "wb") as f:
        f.write(r_file)

    return file.filename


# Convert image size from bytes to height and width
def bytesToArea(file_size: int) -> tuple:
    quality = 50 / 100

    # (Height, Width)
    return (3008, 2008)
