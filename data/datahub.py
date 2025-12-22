import json
import os
import sys
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal

from data.paths import CONFIG_DIR, IMAGES_DIR, CHARACTERS_DIR, PRESETS_DIR, PORTRAITS_DIR, REFERENCE_DIR
from signaling.refresh_character_lists import refresh_character_lists_signal

VALID_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}

data_cache: dict = {}
character_cache: dict = {}

def packaged_path(relative_path: str) -> Path:
    """
    Returns a path to a bundled resource.
    - In PyInstaller builds: uses sys._MEIPASS
    - In dev: falls back to project-ish root (parents[1] from this file)
    """
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return base_dir / relative_path

def _load_json_from_file(json_path: Path) -> dict:
    with open(json_path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)

def _load_all_json_in_dir(source_dir: Path, target_cache: dict, label: str) -> None:
    if not source_dir.exists():
        return
    for filename in os.listdir(source_dir):
        if not filename.endswith(".json"):
            continue
        key = os.path.splitext(filename)[0]
        json_path = source_dir / filename
        try:
            target_cache[key] = _load_json_from_file(json_path)
            print(f"{label}: {filename} loaded...")
        except Exception as exception:
            print(f"{label}: FAILED to load {json_path} ({exception})")

def load_all() -> dict:
    """
    Load order:
      1) Bundled defaults from data/config (inside build, or dev fallback)
      2) Disk overrides from CONFIG_DIR
      3) Disk overrides from PRESETS_DIR
    """
    data_cache.clear()

    # 1) Built-in defaults bundled into the app build
    bundled_config_dir = packaged_path("data/config")
    _load_all_json_in_dir(bundled_config_dir, data_cache, "defaults")

    # 2) User / disk config overrides (wherever CONFIG_DIR points)
    _load_all_json_in_dir(Path(CONFIG_DIR), data_cache, "config")

    # 3) Presets overrides (wherever PRESETS_DIR points)
    _load_all_json_in_dir(Path(PRESETS_DIR), data_cache, "presets")

    return data_cache

def load_characters() -> dict:
    character_cache.clear()

    characters_dir = Path(CHARACTERS_DIR)
    if not characters_dir.exists():
        return character_cache

    for filename in os.listdir(characters_dir):
        if not filename.endswith(".json"):
            continue

        file_path = characters_dir / filename
        try:
            loaded = _load_json_from_file(file_path)
        except Exception as exception:
            print(f"characters: FAILED to load {file_path} ({exception})")
            continue

        character = loaded[0] if isinstance(loaded, list) and loaded else loaded
        if not isinstance(character, dict):
            print(f"characters: unexpected format in {file_path} (expected dict or [dict])")
            continue

        character_id = character.get("nameID") or os.path.splitext(filename)[0]
        character_cache[character_id] = character

    return character_cache

def get_character(character_id, default=None):
    return character_cache.get(character_id, default)

def get_all_characters():
    return list(character_cache.values())

def get_data(key, default=None):
    return data_cache.get(key, default)

def load_image_tree() -> dict:
    image_tree: dict = {}

    def pick_root(disk_path: Path, packaged_relative: str) -> Path:
        if disk_path.exists():
            return disk_path
        bundled = packaged_path(packaged_relative)
        return bundled if bundled.exists() else disk_path

    root_definitions = [
        ("images", pick_root(Path(IMAGES_DIR), "images")),
        ("references", pick_root(Path(REFERENCE_DIR), "references")),
        ("portraits", pick_root(Path(PORTRAITS_DIR), "images/character_portraits")),
    ]

    def add_root_to_tree(root_name: str, root_path: Path) -> None:
        if not root_path.exists():
            return

        root_level = image_tree.setdefault(root_name, {})

        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in VALID_IMAGE_EXTENSIONS:
                continue

            relative_path = file_path.relative_to(root_path)
            path_parts = relative_path.parts
            name_without_extension = file_path.stem

            current_level = root_level
            for folder_name in path_parts[:-1]:
                current_level = current_level.setdefault(folder_name, {})

            current_level[name_without_extension] = str(file_path)

    for root_name, root_path in root_definitions:
        add_root_to_tree(root_name, root_path)

    return image_tree


# Hook your reload signal to character reload
refresh_character_lists_signal.reload_character_data.connect(lambda: load_characters())
