from fastapi import APIRouter, Request, UploadFile, status, HTTPException
from fastapi.templating import Jinja2Templates
from utills import ValidateExtention, ValidateType
from libs.compress import CompressImage, CompressVideo


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


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def compress_file(file: UploadFile):
    is_valid_type, content_type = ValidateType(file.headers['content-type'])
    is_valid_ext, _ = ValidateExtention(file.filename)

    if is_valid_type and is_valid_ext:

        if content_type == "image":
            file_id = CompressImage(file)
            print(file_id)
            file_idx = "test_img.jpg"
            return {"message": "Image upload successful", "fileId": file_idx}

        elif content_type == "video":
            file_id = CompressVideo(file)
            print(file_id)
            file_idx = "test_img.jpg"
            return {"message": "Video upload successful", "fileId": file_idx}

        else:
            raise HTTPException(
                status_code=400, detail="Uploaded file must be an image or a video")
    else:
        raise HTTPException(status_code=400, detail="Not a valid file type")
