from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api import router
from db.db import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

init_db()
