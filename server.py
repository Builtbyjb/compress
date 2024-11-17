from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from routers import compress_routes
import uvicorn
import os
from dotenv import load_dotenv
from utills.clean_up import fileCleanUp
from database.database import create_db_and_tables
from database.database import get_session
from sqlmodel import Session
from typing import Annotated

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

database = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    fileCleanUp()  # Removes uploaded and downloaded files
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
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
