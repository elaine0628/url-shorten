import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, Request
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.schema import ShortenRequest
from models.errcode import ErrorCode
from api.shorten import create_short_url_handler, redirect_url_handler


# --- create_short_url_handler 測試 ---

@patch("api.shorten.insert_url")
@patch("api.shorten.generate_short_url", return_value="abc123")
def test_create_short_url_success(mock_gen, mock_insert):
    request = ShortenRequest(original_url="https://example.com")
    result = create_short_url_handler(request)
    assert result["short_url"] == "abc123"
    assert result["success"] is True
    assert "expiration_date" in result


def test_create_short_url_invalid_url():
    request = ShortenRequest(original_url="ftp://invalid")
    with pytest.raises(HTTPException) as exc:
        create_short_url_handler(request)
    assert exc.value.detail["error_code"] == ErrorCode.INVALID_URL["code"]


def test_create_short_url_too_long():
    long_url = "https://example.com/" + "a" * 2050
    request = ShortenRequest(original_url=long_url)
    with pytest.raises(HTTPException) as exc:
        create_short_url_handler(request)
    assert exc.value.detail["error_code"] == ErrorCode.URL_TOO_LONG["code"]


# --- redirect_url_handler 測試 ---

@patch("api.shorten.fetch_url_by_short")
def test_redirect_url_success(mock_fetch):
    fake_request = MagicMock(Request)
    mock_fetch.return_value = (
        "https://example.com",
        (datetime.now() + timedelta(days=1)).isoformat()
    )

    response = redirect_url_handler(fake_request, "abc123")

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"


@patch("api.shorten.fetch_url_by_short", return_value=None)
def test_redirect_url_not_found(mock_fetch):
    fake_request = MagicMock(Request)
    with pytest.raises(HTTPException) as exc:
        redirect_url_handler(fake_request, "notfound")
    assert exc.value.detail["error_code"] == ErrorCode.SHORT_URL_NOT_FOUND["code"]


@patch("api.shorten.fetch_url_by_short")
def test_redirect_url_expired(mock_fetch):
    fake_request = MagicMock(Request)
    mock_fetch.return_value = (
        "https://example.com",
        (datetime.now() - timedelta(days=1)).isoformat()
    )

    with pytest.raises(HTTPException) as exc:
        redirect_url_handler(fake_request, "expired123")
    assert exc.value.detail["error_code"] == ErrorCode.SHORT_URL_EXPIRED["code"]
