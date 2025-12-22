# data/paths.py
from pathlib import Path
import sys

def get_project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]

PROJECT_ROOT = get_project_root()

DATA_DIR       = PROJECT_ROOT / "data"
CONFIG_DIR     = DATA_DIR / "config"
IMAGES_DIR     = PROJECT_ROOT / "images"
THEMES_DIR     = PROJECT_ROOT / "themes"
OUTPUT_DIR = PROJECT_ROOT / "output"

USER_DIR      = PROJECT_ROOT / 'user_config'
REFERENCE_DIR = USER_DIR / 'character_reference'
CHARACTERS_DIR = USER_DIR / "characters"
PORTRAITS_DIR  = USER_DIR / "character_portraits"
PRESETS_DIR    = USER_DIR / "preset"
SAVE_DIR = USER_DIR / "save"

