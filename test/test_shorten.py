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

    assert result.error_code == ErrorCode.SUCCESS["code"]
    assert result.data["short_url"] == "abc123"
    assert result.data["success"] is True
    assert "expiration_date" in result.data


def test_create_short_url_invalid_url():
    request = ShortenRequest(original_url="ftp://invalid")
    result = create_short_url_handler(request)

    assert result.error_code == ErrorCode.INVALID_URL["code"]
    assert result.data == ErrorCode.INVALID_URL["message"]


def test_create_short_url_too_long():
    long_url = "https://example.com/" + "a" * 2050
    request = ShortenRequest(original_url=long_url)
    result = create_short_url_handler(request)

    assert result.error_code == ErrorCode.URL_TOO_LONG["code"]
    assert result.data == ErrorCode.URL_TOO_LONG["message"]


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
    result = redirect_url_handler(fake_request, "notfound")

    assert result.error_code == ErrorCode.SHORT_URL_NOT_FOUND["code"]
    assert result.data == ErrorCode.SHORT_URL_NOT_FOUND["message"]


@patch("api.shorten.fetch_url_by_short")
def test_redirect_url_expired(mock_fetch):
    fake_request = MagicMock(Request)
    mock_fetch.return_value = (
        "https://example.com",
        (datetime.now() - timedelta(days=1)).isoformat()
    )

    result = redirect_url_handler(fake_request, "expired123")

    assert result.error_code == ErrorCode.SHORT_URL_EXPIRED["code"]
    assert result.data == ErrorCode.SHORT_URL_EXPIRED["message"]
