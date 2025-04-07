from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from server.limiter import limiter
from api.schemas import URLRequest
from db.db import insert_url, fetch_url_by_short
from utils.utils import generate_short_url

router = APIRouter()

@router.post("/shorten")
@limiter.limit("5/minute")
def shorten_url(request: Request, body: URLRequest):
    short_url = generate_short_url()
    expiration_date = (datetime.utcnow() + timedelta(days=30)).isoformat()
    insert_url(str(body.original_url), short_url, expiration_date)
    return {"short_url": short_url, "expiration_date": expiration_date, "success": True}

@router.get("/{short_url}")
@limiter.limit("10/minute")
def redirect_url(request: Request, short_url: str):
    result = fetch_url_by_short(short_url)
    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")
    original_url, expiration_date = result
    if datetime.utcnow() > datetime.fromisoformat(expiration_date):
        raise HTTPException(status_code=410, detail="Short URL expired")
    return RedirectResponse(url=original_url)
