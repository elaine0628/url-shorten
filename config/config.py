import os
import yaml

_settings = None

def load_settings():
    global _settings
    if _settings is None:
        project_root = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(project_root, '..', 'setting', 'setting.yaml')
        config_path = os.path.abspath(config_path)

        with open(config_path, "r") as f:
            _settings = yaml.safe_load(f)

        _settings["app"]["port"] = int(os.getenv("PORT", _settings["app"].get("port", 4000)))

    return _settings


settings = load_settings()
