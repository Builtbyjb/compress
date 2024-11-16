from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from routers import compress_routes
import uvicorn
import os
from dotenv import load_dotenv
from utills.clean_up import fileCleanUp
from database.database import create_db_and_tables

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(compress_routes.router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

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
    fileCleanUp()
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
