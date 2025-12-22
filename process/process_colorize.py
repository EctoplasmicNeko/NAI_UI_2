
from process.base64 import image_to_b64

def prepare_colorize_payload(state):

    image_path = state['main_window']['most_recent_image']
    b64= image_to_b64(image_path)
        
    payload = {
    "req_type": "colorize",
    "prompt": state['colorize']['colorize_prompt'],
    "defry": state['colorize']['colorize_strength_weight'],
    "height": state['main_window']['most_recent_height'],
    "width": state['main_window']['most_recent_width'],
    "image": b64
    }

    return payload

def report(state):
    text = (
        f"image_path = {state['main_window']['most_recent_image']}\n" 
        f"prompt = {state['colorize']['colorize_merged_prompt']},\n"
        f"defry = {state['colorize']['colorize_strength_weight']},\n "
        f"height = {state['main_window']['most_recent_height']},\n "
        f"width = {state['main_window']['most_recent_width']}"
    )
