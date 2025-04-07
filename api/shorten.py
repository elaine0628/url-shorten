from fastapi import Request, HTTPException
from datetime import datetime, timedelta

from db.db import insert_url, fetch_url_by_short
from utils.utils import generate_short_url
from models.errcode import ErrorCode
from models.schema import ShortenRequest, ShortenResponse

def create_short_url_handler(request: ShortenRequest):
    original_url = request.original_url
    if len(original_url) > 2048:
        raise HTTPException(
            status_code=200,
            detail={
                "error_code": ErrorCode.URL_TOO_LONG["code"],
                "message": ErrorCode.URL_TOO_LONG["message"]
            }
        )

    if not original_url or not is_valid_url(original_url):
        raise HTTPException(
            status_code=200,
            detail={
                "error_code": ErrorCode.INVALID_URL["code"],
                "message": ErrorCode.INVALID_URL["message"]
            }
        )

    short_url = generate_short_url()
    expiration_date = (datetime.now() + timedelta(days=30)).isoformat()
    insert_url(str(original_url), short_url, expiration_date)

    return {"short_url": short_url, "expiration_date": expiration_date, "success": True}


def redirect_url_handler(request: Request, short_url: str):
    result = fetch_url_by_short(short_url)
    if not result:
        raise HTTPException(
            status_code=200,
            detail={
                "error_code": ErrorCode.SHORT_URL_NOT_FOUND["code"],
                "message": ErrorCode.SHORT_URL_NOT_FOUND["message"]
            }
        )
    original_url, expiration_date = result
    if datetime.now() > datetime.fromisoformat(expiration_date):
        raise HTTPException(
            status_code=200,
            detail={
                "error_code": ErrorCode.SHORT_URL_EXPIRED["code"],
                "message": ErrorCode.SHORT_URL_EXPIRED["message"]
            }
        )
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=original_url)


def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")
