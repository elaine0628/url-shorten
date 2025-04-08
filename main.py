import os
import yaml
import uvicorn

from config.config import settings
from server.server import app

if __name__ == "__main__":
    port = settings["app"]["port"]
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
