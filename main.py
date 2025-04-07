import os
import yaml
import uvicorn

from server.server import app

def load_settings():
    with open("setting/setting.yaml", "r") as f:
        return yaml.safe_load(f)

settings = load_settings()

# 優先使用環境變數，否則使用設定檔中的設定
port = int(os.getenv("PORT", settings["app"].get("port", 4000)))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
