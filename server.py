from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import compress_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))


app = FastAPI()
app.include_router(compress_routes.router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/compressed", StaticFiles(directory="compressed"), name="compressed")

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


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
