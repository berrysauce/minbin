import os

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .utils import db
from .config import Config

app = FastAPI(
    docs_url=None,  # Disable OpenAPI docs
    redoc_url=None,  # Disable ReDoc docs
)
r = db.get_redis_client()

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def post_paste(request: Request):
    paste_id = os.urandom(2).hex()
    paste_body = await request.body()
    paste_expiry = Config.DEFAULT_EXPIRY * 60  # convert minutes to seconds
    await r.set(paste_id, paste_body.decode(), ex=paste_expiry)
    return f"{paste_id}"


@app.get("/{paste_id}", response_class=HTMLResponse)
async def get_paste(paste_id: str, request: Request):
    paste_body = await r.get(paste_id)
    paste_expiry = await r.ttl(paste_id)

    # convert seconds to minutes for display
    paste_expiry = paste_expiry // 60  # round down to nearest minute

    if paste_body is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={"paste_id": paste_id},
            status_code=404,
        )
    return templates.TemplateResponse(
        request=request,
        name="paste.html",
        context={
            "paste_url": f"{Config.APP_DOMAIN}/{paste_id}",
            "paste_body": paste_body,
            "paste_expiry": paste_expiry,
        },
    )


@app.get("/health")
async def get_health():
    await r.set("health", "ok")
    msg = await r.get("health")
    return {"health": msg}
