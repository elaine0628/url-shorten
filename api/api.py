# api/api.py

from fastapi import APIRouter, Request
from models.schema import ShortenRequest, ShortenResponse, APIResponse
from .shorten import create_short_url_handler, redirect_url_handler

router = APIRouter()

@router.post(
    "/shorten",
    response_model=ShortenResponse,
    responses={
        200: {"model": APIResponse},
    },
)
def create_short_url(request: ShortenRequest):
    return create_short_url_handler(request)

@router.get(
    "/{short_url}",
    responses={
        200: {"model": APIResponse},
    },
)
def redirect_url(request: Request, short_url: str):
    return redirect_url_handler(request, short_url)