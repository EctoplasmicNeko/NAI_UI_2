from pathlib import Path
import json
from data.paths import SAVE_DIR
config_file_path = SAVE_DIR / "save.json"

def save_config(state):
    with config_file_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def load_config():
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def update_config(path: str, value):
    """
    Update a single value in save.json using a dot-separated path, e.g.:
    update_config_value("global_prompt.image_width", 1024)
    """
    # Load existing config or start with empty
    if config_file_path.exists():
        with config_file_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    # Walk/create nested dicts
    keys = path.split(".")
    current = config
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    # Set the final value
    current[keys[-1]] = value

    # Save back to disk
    with config_file_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)