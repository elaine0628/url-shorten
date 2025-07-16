import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from models.schema import ShortenRequest, APIResponse
from models.errcode import ErrorCode
from api.shorten import create_short_url_handler, redirect_url_handler


# --- create_short_url_handler 測試 ---

@patch("api.shorten.insert_url")
@patch("api.shorten.generate_short_url", return_value="abc123")
def test_create_short_url_success(mock_gen, mock_insert):
    request = ShortenRequest(original_url="https://example.com")
    result = create_short_url_handler(request)

    assert result.error_code == ErrorCode.SUCCESS["code"]
    assert isinstance(result.data, dict)
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

    assert isinstance(response, RedirectResponse)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"


@patch("api.shorten.fetch_url_by_short", return_value=None)
def test_redirect_url_not_found(mock_fetch):
    fake_request = MagicMock(Request)
    result = redirect_url_handler(fake_request, "notfound")

    assert isinstance(result, APIResponse)
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

    assert isinstance(result, APIResponse)
    assert result.error_code == ErrorCode.SHORT_URL_EXPIRED["code"]
    assert result.data == ErrorCode.SHORT_URL_EXPIRED["message"]


# --- is_valid_url 測試 ---

@patch("api.shorten.insert_url")
@patch("api.shorten.generate_short_url", return_value="abc123")
def test_valid_http_url(mock_gen, mock_insert):
    request = ShortenRequest(original_url="http://example.com")
    result = create_short_url_handler(request)
    assert result.error_code == ErrorCode.SUCCESS["code"]


@patch("api.shorten.insert_url")
@patch("api.shorten.generate_short_url", return_value="abc123")
def test_valid_https_url(mock_gen, mock_insert):
    request = ShortenRequest(original_url="https://example.com")
    result = create_short_url_handler(request)
    assert result.error_code == ErrorCode.SUCCESS["code"]


def test_invalid_ftp_url():
    request = ShortenRequest(original_url="ftp://example.com")
    result = create_short_url_handler(request)
    assert result.error_code == ErrorCode.INVALID_URL["code"]


def test_empty_url():
    request = ShortenRequest(original_url="")
    result = create_short_url_handler(request)
    assert result.error_code == ErrorCode.INVALID_URL["code"]
