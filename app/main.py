import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .utils.db import get_redis_client
from .utils.other import get_version
from .config import Config

app = FastAPI(
    title="minbin",
    summary="a minimal, ephemeral pastebin service",
    description="a minimal, ephemeral pastebin service",
    version=get_version(),
    openapi_url="/openapi",
    docs_url=None,  # disable OpenAPI docs
    redoc_url=None,  # disable ReDoc docs
)
r = get_redis_client()

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def post_paste(request: Request):
    # parse paste body
    paste_body = await request.body()
    if not paste_body or len(paste_body) > Config.MAX_PASTE_SIZE:
        return PlainTextResponse(
            "Paste body is empty or exceeds maximum size.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # generate paste ID, set expiry, and store in Redis
    paste_id = str(uuid.uuid4())[:4]
    paste_expiry = Config.PASTE_EXPIRY * 60  # convert minutes to seconds
    await r.set(paste_id, paste_body.decode(), ex=paste_expiry)

    return f"{paste_id}"


@app.get("/raw/{paste_id}", response_class=PlainTextResponse)
async def get_raw_paste(paste_id: str, request: Request):
    paste_body = await r.get(paste_id)

    if paste_body is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paste with ID '{paste_id}' not found.",
        )

    return paste_body


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
            status_code=404,
        )

    return templates.TemplateResponse(
        request=request,
        name="paste.html",
        context={
            "paste_id": paste_id,
            "paste_url": f"{Config.APP_DOMAIN}/{paste_id}",
            "paste_body": paste_body,
            "paste_expiry": paste_expiry,
        },
    )
