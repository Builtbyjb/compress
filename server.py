from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn


HOST = "127.0.0.1"
PORT = 8000


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

auth = True


@app.get("/")
async def index(request: Request):
    if auth:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={}
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={}
        )


@app.get("/compress")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compress.html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
