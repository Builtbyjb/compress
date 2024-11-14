from fastapi import APIRouter, Request, UploadFile, status, HTTPException
from fastapi.templating import Jinja2Templates
from utills import ValidateExtention, ValidateType, saveFile, changeDisplayFileName
from libs.compress import CompressImage, CompressVideo
from logger import logger


router = APIRouter(
    prefix="/compress",
    tags=["Compress"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/", status_code=status.HTTP_200_OK)
def get_compress_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compress.html",
    )


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def compress_file(file: UploadFile):
    is_valid_type, content_type = ValidateType(file.headers['content-type'])
    is_valid_ext, ext = ValidateExtention(file.filename)

    if is_valid_type and is_valid_ext:

        # Compress image files
        if content_type == "image" or content_type == "application":
            file_name = await saveFile(file)
            message, new_file_name, new_file_size = CompressImage(
                file_name, ext)

            if message == "Success":
                return {
                    "message": message,
                    "fileDisplayName": file.filename,
                    "fileDownloadName": new_file_name,
                    "compressedFileSize": new_file_size,
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=message
                )

        # Compress video files
        elif content_type == "video":
            file_name, original_filename = await saveFile(file)
            message, new_file_name, new_file_size = await CompressVideo(file_name)
            display_name = changeDisplayFileName(original_filename, 'mp4')

            if message == "Success":
                return {
                    "message": message,
                    "fileDisplayName": display_name,
                    "fileDownloadName": new_file_name,
                    "compressedFileSize": new_file_size,
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=message
                )
        else:
            logger.info("Uploadded file must be an image or a video")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must be an image or a video"
            )
    else:
        logger.info("Not a valid file type")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not a valid file type"
        )
