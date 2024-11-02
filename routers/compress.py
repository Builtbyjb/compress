from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/compress",
    tags=["items"],

)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_compress_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compress.html",
    )


@router.post("/")
async def compress_file():
    return "success"