from fastapi import APIRouter, Request, UploadFile, status
from fastapi.templating import Jinja2Templates
from utills import is_valid_ext, is_valid_type
import time
import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


router = APIRouter(
    prefix="/compress",
    tags=["Compress"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_compress_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compress.html",
    )


@router.post("/")
async def compress_file(file: UploadFile) -> dict:
    print("'''")
    print(file.filename)
    print(file.headers['content-type'])
    print(f"valid extention: {is_valid_ext(file.filename)}")
    print(f"valid type: {is_valid_type(file.headers['content-type'])}")
    print("'''")
    # original_filename = file.filename
    # return {"message": "Upload successful", "filename": original_filename}
    return {"message": "Upload successful"}
