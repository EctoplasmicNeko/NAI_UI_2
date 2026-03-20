import json
import hashlib
from pathlib import Path

import base64
import requests


import requests

from data.paths import ENCODES_DIR
from process.base64 import image_to_b64


def compute_image_hash(image_path: Path) -> str:
    sha256 = hashlib.sha256()
    with image_path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def extract_encoding_from_nai_response(response_json: dict) -> str:
    try:
        encodings_by_model = response_json["encodings"]
        model_bucket_dict = next(iter(encodings_by_model.values()))
        encoding_entry = next(iter(model_bucket_dict.values()))
        encoding_value = encoding_entry["encoding"]
    except Exception as exc:
        raise RuntimeError(f"Failed to extract encoding from NAI response: {exc}")

    if not isinstance(encoding_value, str) or not encoding_value:
        raise RuntimeError("Encoding value missing or invalid in NAI response")

    return encoding_value



def encode_vibe_with_nai(image_b64: str, model_value: str, information_extracted_value: float, api_token: str) -> str:
    url = "https://image.novelai.net/ai/encode-vibe"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json", "Origin": "https://novelai.net", "Referer": "https://novelai.net/"}
    payload = {"model": model_value, "image": image_b64, "information_extracted": information_extracted_value}

    response = requests.post(url, json=payload, headers=headers, timeout=120)

    content_type = (response.headers.get("Content-Type") or "").lower()

    if response.status_code != 200:
        raise RuntimeError(f"NAI encode failed ({response.status_code}): {response.text}")

    # If it really is JSON, extract from JSON.
    if "application/json" in content_type or (response.text and response.text.lstrip().startswith("{")):
        response_json = response.json()
        return extract_encoding_from_nai_response(response_json)

    # Otherwise: treat as raw vibe-asset bytes and base64 it yourself.
    encoding_b64 = base64.b64encode(response.content).decode("ascii")
    if not encoding_b64:
        raise RuntimeError("NAI encode returned empty binary body")

    return encoding_b64




def write_vibe_cache_json(cache_path: Path, image_hash: str, model_value: str, information_extracted_value: float, encoding_b64: str) -> None:
    cache_data = {"image_hash": image_hash, "model": model_value, "information_extracted": float(information_extracted_value), "encoding": encoding_b64}
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8") as file_handle:
        json.dump(cache_data, file_handle, indent=2, ensure_ascii=False)


def identify_vibe_images(state):
    """
    Ensures all selected vibe images have cached encodings on disk, then returns two lists:
      - encodings: list[str] (base64 encoding blobs)
      - information_extracted_values: list[float] (one per encoding)

    Expected state shape:
      state["reference_image_paths"] -> list[str|Path]
      state["generate"]["model"] -> str
      state["vibe"][i]["information_extracted"] -> float
      state["auth"]["api_token"] -> str
    """
    encodings = []

    model_value = state["generate"]["model"]
    api_token = state["settings"]["API_key"]

    for index, path in enumerate(state["vibe"]["reference_image_paths"]):
        image_path = Path(path)
        if not image_path.exists():
            raise FileNotFoundError(f"Vibe image not found: {image_path}")

        information_extracted_value = float(state["vibe"]["reference_information_extracted"][index])
        info_str = f"{information_extracted_value:.2f}"

        image_hash = compute_image_hash(image_path)
        vibe_identifier = f"{model_value}__{image_hash}__info-{info_str}"
        cache_path = ENCODES_DIR / f"{vibe_identifier}.json"

        if cache_path.exists():
            with cache_path.open("r", encoding="utf-8") as file_handle:
                cached_data = json.load(file_handle)
            encoding_b64 = cached_data.get("encoding")
            if not isinstance(encoding_b64, str) or not encoding_b64:
                raise RuntimeError(f"Cached encode JSON missing 'encoding': {cache_path}")
        else:
            image_b64 = image_to_b64(image_path)
            encoding_b64 = encode_vibe_with_nai(
                image_b64=image_b64,
                model_value=model_value,
                information_extracted_value=information_extracted_value,
                api_token=api_token,
            )
            write_vibe_cache_json(
                cache_path=cache_path,
                image_hash=image_hash,
                model_value=model_value,
                information_extracted_value=information_extracted_value,
                encoding_b64=encoding_b64,
            )

        encodings.append(encoding_b64)

    return encodings