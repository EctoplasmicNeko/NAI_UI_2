import io
import base64
from PIL import Image
from PIL import Image
import io, base64
from pathlib import Path


def image_to_b64(reference_path):
    """Return base64 PNG of the original image (no padding, no resize)."""
    if not reference_path:
        return None

    img = Image.open(reference_path).convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG", quality=95)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")




def padded_image_to_b64(reference_path,
                        portrait_size=(1024, 1536),
                        landscape_size=(1536, 1024),
                        square_size=(1472, 1472),
                        debug_output_dir= r"C:\Users\jesse\OneDrive\Desktop\NAI_UI_2"):
    """Return base64 PNG of the image padded to portrait/landscape/square.
       If debug_output_dir is given, save padded image there as <stem>_padded.png.
    """
    if not reference_path:
        return None

    img = Image.open(reference_path).convert("RGB")
    width, height = img.size

    # Choose target size based on orientation
    if width == height:
        target_w, target_h = square_size
    elif height > width:
        target_w, target_h = portrait_size
    else:
        target_w, target_h = landscape_size

    # Scale proportionally to fit inside target
    scale = min(target_w / width, target_h / height)
    new_w, new_h = int(width * scale), int(height * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Create black background and paste centered
    new_img = Image.new("RGB", (target_w, target_h), (0, 0, 0))
    left = (target_w - new_w) // 2
    top = (target_h - new_h) // 2
    new_img.paste(resized, (left, top))

    # --- Save debug image if directory provided ---
    if debug_output_dir:
        debug_dir = Path(debug_output_dir)
        debug_dir.mkdir(parents=True, exist_ok=True)

        original_stem = Path(reference_path).stem
        save_path = debug_dir / f"{original_stem}_padded.png"

        new_img.save(save_path, format="PNG")
        print(f"[DEBUG] Saved padded image to: {save_path}")

    # --- Encode to base64 ---
    buffer = io.BytesIO()
    new_img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return b64_str

