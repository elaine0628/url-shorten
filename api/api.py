# api/api.py

from fastapi import APIRouter, Request
from server.limiter import limiter
from models.schema import ShortenRequest, ShortenResponse
from .shorten import create_short_url_handler, redirect_url_handler

router = APIRouter()

@router.post("/shorten", response_model=ShortenResponse)
def create_short_url(request: ShortenRequest):
    return create_short_url_handler(request)

@router.get("/{short_url}")
@limiter.limit("10/minute")
def redirect_url(request: Request, short_url: str):
    return redirect_url_handler(request, short_url)