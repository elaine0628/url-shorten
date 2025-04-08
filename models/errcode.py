class ErrorCode:
    SUCCESS = {
        "code": 0,
        "message": "Success",
    }

    INVALID_URL = {
        "code": 600,
        "message": "Invalid URL format",
    }

    URL_TOO_LONG = {
        "code": 601,
        "message": "URL is too long",
    }

    SHORT_URL_NOT_FOUND = {
        "code": 602,
        "message": "Short URL not found",
    }

    SHORT_URL_EXPIRED = {
        "code": 603,
        "message": "Short URL expired",
    }


