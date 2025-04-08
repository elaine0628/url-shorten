from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class ShortenRequest(BaseModel):
    original_url: str

class ShortenResponse(BaseModel):
    short_url: str
    expiration_date: datetime
    success: bool

class APIResponse(BaseModel):
    error_code: int
    data: Optional[Any]