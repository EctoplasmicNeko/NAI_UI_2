
import json
from pathlib import Path
from PIL import Image, PngImagePlugin

def write_custom_metadata(input_path, output_path, key, value):
    """
    Copy a PNG from input_path to output_path, preserving existing text metadata,
    and add/update a custom text key with value (converted to str).

    key    -> e.g. "NAI_UI_2" or "NAI_UI_2_state"
    value  -> str or anything JSON-serializable
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with Image.open(input_path) as image:
        # Build a new PngInfo, copying existing info over
        pnginfo = PngImagePlugin.PngInfo()
        for k, v in image.info.items():
            # v might be bytes or str
            if isinstance(v, bytes):
                try:
                    v = v.decode("utf-8", errors="ignore")
                except Exception:
                    continue
            if isinstance(v, str):
                pnginfo.add_text(k, v)

        # Prepare our value
        if not isinstance(value, str):
            # default: tuck it in as JSON
            value = json.dumps(value, ensure_ascii=False)

        pnginfo.add_text(key, value)

        # Save with metadata
        image.save(output_path, pnginfo=pnginfo)


def write_custom_metadata(input_path, output_path, key, value):
    """
    Copy a PNG from input_path to output_path, preserving existing text metadata,
    and add/update a custom text key with value (converted to str).
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with Image.open(input_path) as image:
        pnginfo = PngImagePlugin.PngInfo()
        for k, v in image.info.items():
            if isinstance(v, bytes):
                try:
                    v = v.decode("utf-8", errors="ignore")
                except Exception:
                    continue
            if isinstance(v, str):
                pnginfo.add_text(k, v)

        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)

        pnginfo.add_text(key, value)
        image.save(output_path, pnginfo=pnginfo)


def prepare_metadata(state, payload):
    character_number = state['global_prompt']['character_number']

    generate = {
        "model": state['generate']['model_name'],
        "sampler": state['generate']['sampler_name'],
        "schedule": state['generate']['schedule_name'],
        "steps": state['generate']['steps'],
        "seed": payload['parameters']['seed'],
        "scale": state['generate']['scale'],
        "rescale": state['generate']['rescale'],
        "cfg": state['generate']['cfg'],
        "legacy_v3": state['generate']['legacy_v3'],
        "legacy_v4": state['generate']['legacy_v4'],
        "SMEA": state['generate']['SMEA'],
        "DYN": state['generate']['DYN'],
        "variety+": state['generate']['variety+'],
        "decrisp": state['generate']['decrisp'],
        "brownian": state['generate']['brownian'],
        "size_name": state['generate']['size_name'],
    }

    global_prompt = {
        "global_positive_prompt": state['global_prompt']['global_positive_prompt'],
        "global_negative_prompt": state['global_prompt']['global_negative_prompt'],
        "global_positive_preset_name": state['global_prompt']['global_positive_preset_name'],
        "global_negative_preset_name": state['global_prompt']['global_negative_preset_name'],
        "global_positive_preset_tags": state['global_prompt']['global_positive_preset_tags'],
        "global_negative_preset_tags": state['global_prompt']['global_negative_preset_tags'],
        "character_number": state['global_prompt']['character_number'],
    }

    # ---- Characters ----
    characters = {}
    for index in range(1, character_number + 1):
        key = f"character_{index}"
        character = {
            "character": state[key]['character'],
            "character_positive_prompt": state[key]['character_positive_prompt'],
            "character_negative_prompt": state[key]['character_negative_prompt'],
            "character_coordinate_button": state[key]['character_coordinate_button'],
            "character_preset_positive": state[key]['character_preset_positive'],
            "character_preset_negative": state[key]['character_preset_negative'],
            "character_preset_global_positive": state[key]['character_preset_global_positive'],
            "character_preset_global_negative": state[key]['character_preset_global_negative'],
            "character_outfit_preset_positive": state[key]['character_outfit_preset_positive'],
            "character_outfit_preset_negative": state[key]['character_outfit_preset_negative'],
            "most_recent_outfit": state[key]['most_recent_outfit'],
        }
        characters[key] = character

    # ---- Optional reference block (v4.5 only, when present) ----
    reference = None
    params = payload.get("parameters", {})
    director_images = params.get("director_reference_images")

    if director_images:
        # pull settings from character_1 in state
        char1 = state.get("character_1", {})
        reference = {
            "referenceb64": director_images,
            "character_reference_style_aware": char1.get("character_reference_style_aware"),
            "character_reference_fidelity": char1.get("character_reference_fidelity"),
            "character_reference_strength": char1.get("character_reference_strength"),
        }

    return {
        "characters": characters,
        "generate": generate,
        "global_prompt": global_prompt,
        "reference": reference,  # None if no director reference
    }
