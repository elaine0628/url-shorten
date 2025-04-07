from pydantic import BaseModel
from datetime import datetime

class ShortenRequest(BaseModel):
    original_url: str

class ShortenResponse(BaseModel):
    short_url: str
    expiration_date: datetime
    success: bool