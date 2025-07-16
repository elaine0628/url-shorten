import os
import yaml
import uvicorn

from config.config import settings
from server.server import app

if __name__ == "__main__":
    port = settings["app"]["port"]
    # 在除錯模式下，使用 reload=False 避免模組重載
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
