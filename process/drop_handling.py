import json
from pathlib import Path
from PIL import Image
from windows.error import Error

def is_valid_image_file(file_path, allowed_extensions=None):
    """
    Return True if file_path has an allowed image extension.
    allowed_extensions should be a set/list of lowercase extensions like {'.png', '.jpg'}.
    """
    if allowed_extensions is None:
        allowed_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    path_object = Path(file_path)
    file_suffix = path_object.suffix.lower()

    return file_suffix in allowed_extensions


def load_nai_raw_info(image_path):
    """
    Return a dict of PNG info fields as strings.
    Only looks at image.info (no EXIF).
    Example keys: 'Title', 'Description', 'Software', 'Source', 'Generation time', 'Comment'
    """
    image_path = Path(image_path)
    info_dict = {}

    with Image.open(image_path) as image:
        if hasattr(image, "info") and image.info:
            for key, value in image.info.items():
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8", errors="ignore")
                    except Exception:
                        continue
                if isinstance(value, (str, int, float)):
                    info_dict[key] = str(value)

    return info_dict


def load_nai_comment_json(image_path):
    """
    Parse the JSON stored in info['Comment'] and return it as a dict,
    or None if missing / invalid.
    """
    info_dict = load_nai_raw_info(image_path)
    comment = info_dict.get("Comment")
    if comment is None:
        return None

    comment = comment.strip()
    if not ((comment.startswith("{") and comment.endswith("}")) or (comment.startswith("[") and comment.endswith("]"))):
        return None

    try:
        return json.loads(comment)
    except json.JSONDecodeError:
        return None
    

def load_custom_json(image_path):
    """
    Parse the JSON stored in info['Comment'] and return it as a dict,
    or None if missing / invalid.
    """
    info_dict = load_nai_raw_info(image_path)
    custom = info_dict.get("NAI_UI_2")
    if custom is None:
        return None

    custom = custom.strip()
    if not ((custom.startswith("{") and custom.endswith("}")) or (custom.startswith("[") and custom.endswith("]"))):
        return None

    try:
        return json.loads(custom)
    except json.JSONDecodeError:
        return None


def get_nai_comment_value(image_path, *key_path, default=None):
    """
    Get a value from the Comment JSON using a key path.

    Examples:
        get_nai_comment_value(path, "prompt")
        get_nai_comment_value(path, "steps")
        get_nai_comment_value(path, "v4_prompt", "caption", "base_caption")

    Returns `default` if anything is missing.
    """
    data = load_nai_comment_json(image_path)
    if data is None:
        return default

    current = data
    for key in key_path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current


def parse_nai_source_field(source_string):
    """
    Parse info['Source'], e.g. 'NovelAI Diffusion V4.5 4BDE2A90'
    into (model_label, model_hash).

    Returns (None, None) if it can't parse.
    """
    if not source_string:
        return None, None

    parts = source_string.strip().split()
    if len(parts) < 2:
        return None, None

    # assume last token is the hash, everything before that is the label
    model_hash = parts[-1]
    model_label = " ".join(parts[:-1])
    return model_label, model_hash

def get_character_dict(comment_json, index):
    """
    Extract character prompt info from the comment JSON for a given character index.
    """
    try:
        return {
            'character_positive_prompt': comment_json["v4_prompt"]["caption"]["char_captions"][index]["char_caption"],
            'character_negative_prompt': comment_json["v4_negative_prompt"]["caption"]["char_captions"][index]["char_caption"],
            'character_x_pos': comment_json["v4_prompt"]["caption"]["char_captions"][index]["centers"][0]["x"],
            'character_y_pos': comment_json["v4_prompt"]["caption"]["char_captions"][index]["centers"][0]["y"],
        
        }
    except (KeyError, IndexError, TypeError):
        return {
            'positive_character_prompt': "",
            'negative_character_prompt': "",
            'character_x_pos': None,
            'character_y_pos': None,
        }


def get_metadata(image_path):

    info_dict = load_nai_raw_info(image_path) #check that image has some metadata
    
    if not info_dict:
        Error(None, "The dropped file does not contain any PNG metadata.")
        return None
    
    comment_json = load_nai_comment_json(image_path)

    if comment_json is None:
        Error(None, "The dropped image does not contain valid NovelAI metadata.")
        return None
    
    if comment_json['request_type'] == "NativeInfillingRequest":
        Error(None, "Inpainting images are not supported for metadata import.")
        return None

    custom_dict = load_custom_json(image_path) #try to load NAI_UI_2 custom metadata

    if not custom_dict:
        print("No NAI_UI_2 metadata found in the image, fallback to NovelAI metadata.")
        return 'native', get_imported_image_metadata_native(image_path, info_dict, comment_json) #fallback to native metadata parsing
    else:
        print("NAI_UI_2 metadata found in the image, using custom metadata.")
        character_count = len(custom_dict["characters"])
        print(f"Detected {character_count} characters in the image metadata.")
        return 'custom', custom_dict
    

def get_imported_image_metadata_native(image_path, info_dict, comment_json):

    source = info_dict.get("Source", "")
    model_label, model_hash = parse_nai_source_field(source)

    if model_label.startswith("Stable Diffusion XL"):
        print(f"V3/SDXL image detected, no character data present.")
        character_count = 0
    else:
        character_count = len(comment_json["v4_prompt"]["caption"]["char_captions"])
        print(f"Detected {character_count} characters in the image metadata.")

    top_level = {
        # raw info
        "title": info_dict.get("Title"),
        "description": info_dict.get("Description"),
        "software": info_dict.get("Software"),
        "source": source,
        "generation_time": info_dict.get("Generation time"),

        # parsed model info
        "model_label": model_label,              # e.g. "NovelAI Diffusion V4.5"
        "model_hash": model_hash,                # e.g. "4BDE2A90"
    }

    generate = {
        'steps': comment_json.get("steps"),
        'height': comment_json.get("height"),
        'width': comment_json.get("width"),
        'scale': comment_json.get("scale"),
        'cfg_rescale': comment_json.get("cfg_rescale"),
        'seed': comment_json.get("seed"),
        'noise_schedule': comment_json.get("noise_schedule"),
        'legacy_v3_extend': comment_json.get("legacy_v3_extend", False),
        'sampler': comment_json.get("sampler"),
        'dynamic_thresholding': comment_json.get("dynamic_thresholding", False),
        'sm': comment_json.get("sm", False),
        'sm_dyn': comment_json.get("sm_dyn", False),
        'skip_cfg_above_sigma': comment_json.get("skip_cfg_above_sigma", False),
        'prefer_brownian': comment_json.get("prefer_brownian", False),
        'legacy_uc': comment_json.get("legacy_uc", False),

    }

    global_prompt = {
        'global_positive_prompt': comment_json.get("prompt"),
        'global_negative_prompt': comment_json.get("uc"),
        'character_number': character_count,
    }

    characters = {}
    for i in range(character_count):
        characters[f'character_{i+1}'] = get_character_dict(comment_json, i)

    return {
        'top_level': top_level,
        'global_prompt': global_prompt,
        'generate': generate,
        'characters': characters,
    }


