import logging
import time
import colorlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
import uvicorn


from sqlalchemy import text
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.database.db import get_db, get_redis
from src.routes import contacts, auth, users

logger = logging.getLogger(f"{settings.app_name}")
logger.setLevel(logging.DEBUG if settings.app_mode == "dev" else logging.INFO)
handler = colorlog.StreamHandler()
handler.setLevel(logging.DEBUG if settings.app_mode == "dev" else logging.INFO)
handler.setFormatter(colorlog.ColoredFormatter("%(yellow)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("lifespan before")
    try:
        await startup()
    except redis.ConnectionError as err:
        logger.error(f"redis err: {err}")
    except Exception as err:
        logger.error(f"other app err: {err}")
    yield
    logger.debug("lifespan after")


# lifespan = None


app = FastAPI(lifespan=lifespan)  # type: ignore


# @app.on_event("startup")
async def startup():
    await FastAPILimiter.init(get_redis())
    logger.debug("startup done")


origins = ["http://localhost:3002"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def add_static(_app):
    _app.mount(path="/static", app=StaticFiles(directory=settings.STATIC_DIRECTORY), name="static")
    _app.mount(path="/sphinx", app=StaticFiles(directory=settings.SPHINX_DIRECTORY, html=True), name="sphinx")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tilte": f"{settings.app_version.upper()} APP {settings.app_name.upper()}"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": f"Welcome to FastAPI on Howe Work 13 APP: {settings.app_name.upper()}!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


app.include_router(
    contacts.router,
    prefix="/api",
    dependencies=[Depends(RateLimiter(times=settings.reate_limiter_times, seconds=settings.reate_limiter_seconds))],
)
app.include_router(
    auth.router,
    prefix="/api/auth",
    dependencies=[Depends(RateLimiter(times=settings.reate_limiter_times, seconds=settings.reate_limiter_seconds))],
)
app.include_router(users.router, prefix="/api")

add_static(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
