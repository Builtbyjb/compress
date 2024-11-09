import uuid
import os
from fastapi import UploadFile
import math
import re

BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4", "heic"]


# Valid file extention
def ValidateExtention(file_name: str) -> tuple[bool, str]:
    ext_list = file_name.lower().split(".")
    idx = len(ext_list) - 1
    if ext_list[idx] in ALLOWED_EXT:
        return (True, ext_list[idx])
    else:
        return (False, "")


ALLOWED_TYPE = ["image", "video", "application"]


# Confirm content type
def ValidateType(content_type: str) -> tuple[bool, str]:
    type_re = re.compile(r'(^[a-z]+)/')
    type_match = type_re.search(content_type)
    type_s = type_match.group(1)

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


# Reduce file height and width
def compressSize(file_size: tuple[int, int], quality: int) -> tuple[int, int]:
    compress_percentage = quality / 100

    width = math.floor(file_size[0] * compress_percentage)
    height = math.floor(file_size[1] * compress_percentage)

    # (Width, Height)
    return (width, height)


# Converts the file area to bytes
def areaToBytes(area: tuple[int, int]) -> int:

    return 1_433_451
