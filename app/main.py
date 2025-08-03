"""
minbin - a minimal, ephemeral pastebin service
"""

import os
import json
from typing import Optional

from fastapi import FastAPI, Request, status, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import Config
from app.utils.db import get_redis_client
from app.utils.other import get_version

app = FastAPI(
    title="minbin",
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
    """Get the index page."""

    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def post_paste(
    request: Request,
    once: Optional[str] = Query(
        default=None,
        description="If true, the paste will self-destruct after one view.",
    ),
):
    """Create a new paste."""

    # parse paste body
    paste_body = await request.body()
    if not paste_body or len(paste_body) > Config.MAX_PASTE_SIZE:
        return PlainTextResponse(
            "Paste body is empty or exceeds maximum size.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # generate paste ID, set expiry, and store in Redis
    paste_id = os.urandom(2).hex()  # generate a random 2-byte hex ID
    paste_expiry = Config.PASTE_EXPIRY * 60  # convert minutes to seconds
    paste_content = json.dumps(
        {
            "body": paste_body.decode(),
            "once": bool(once is not None),
        }
    )
    await r.set(paste_id, paste_content, ex=paste_expiry)

    return f"{Config.APP_DOMAIN}/{paste_id}"


@app.get("/raw/{paste_id}", response_class=PlainTextResponse)
async def get_raw_paste(paste_id: str):
    """Get the raw paste content by ID."""

    paste_content = await r.get(paste_id)

    if paste_content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paste with ID '{paste_id}' not found.",
        )

    paste_content = json.loads(paste_content)
    paste_body = paste_content.get("body", "")

    if paste_content.get("once", False):
        # if the paste is a one-time view, delete it after retrieval
        await r.delete(paste_id)

    return paste_body


@app.get("/{paste_id}", response_class=HTMLResponse)
async def get_paste(paste_id: str, request: Request):
    """Get the paste content by ID."""

    paste_content = await r.get(paste_id)
    paste_expiry = await r.ttl(paste_id)

    # convert seconds to minutes for display
    paste_expiry = paste_expiry // 60  # round down to nearest minute

    if paste_content is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            status_code=404,
        )

    paste_content = json.loads(paste_content)
    paste_body = paste_content.get("body", "")

    if paste_content.get("once", False):
        # if the paste is a one-time view, delete it after retrieval
        await r.delete(paste_id)

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
