
from process.base64 import image_to_b64

def prepare_emotion_payload(state):

    image_path = state['main_window']['most_recent_image']
    b64= image_to_b64(image_path)
        
    payload = {
    "req_type": "emotion",
    "prompt": state['emotion']['emotion_merged_prompt'],
    "defry": state['emotion']['emotion_strength_weight'],
    "height": state['main_window']['most_recent_height'],
    "width": state['main_window']['most_recent_width'],
    "image": b64
    }

    return payload

def report(state):
    text = (
        f"image_path = {state['main_window']['most_recent_image']}\n" 
        f"prompt = {state['emotion']['emotion_merged_prompt']},\n"
        f"defry = {state['emotion']['emotion_strength_weight']},\n "
        f"height = {state['main_window']['most_recent_height']},\n "
        f"width = {state['main_window']['most_recent_width']}"
    )
