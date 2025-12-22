import datetime
from process.process_generate import prepare_generate_payload
from process.process_emotion import prepare_emotion_payload
from process.process_colorize import prepare_colorize_payload
from process.metadata import write_custom_metadata
from process.CompletionSignaler import completion_signaler
from data.paths import OUTPUT_DIR
import requests
import os
import zipfile
import uuid
import time
from datetime import datetime
from hydrus.sidecar_write import write_hydrus_sidecar

def run_process(state):
    header = prepare_header(state)
    request = state['workflow']['request_name']

    if request == 'generate':
        payload, metadata = prepare_generate_payload(state)
        file_path = post_to_backend(payload, header, state)
        if file_path is None:
            return None  # failed, UI already reset via signal
        write_custom_metadata(file_path, file_path, "NAI_UI_2", metadata)

    elif request == 'emotion':
        payload = prepare_emotion_payload(state)
        file_path = post_to_backend(payload, header, state)
        if file_path is None:
            return None  # failed, UI already reset via signal

    elif request == 'colorize':
        payload = prepare_colorize_payload(state)
        file_path = post_to_backend(payload, header, state)
        if file_path is None:
            return None  # failed, UI already reset via signal
    
    if state['settings']['enable_hydrus_sidecar']:
        write_hydrus_sidecar(file_path, state)
        
    return file_path


def prepare_header(state):
    header = {
    "Authorization": f"Bearer {state['settings']['API_key']}",
    "Content-Type": "application/json"
    }
    return header
    
def post_to_backend(payload, header, state):
    retries = 0
    success = False
    MAX_RETRIES = 3
    RETRY_DELAY = 5

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    last_error = None
    file_path = None  # only set when we actually succeed

    while not success and retries < MAX_RETRIES:
        try:
            with requests.post(
                url=state['workflow']['request_url'],
                json=payload,
                headers=header,
                stream=True,
                timeout=20
            ) as response:

                # raise if not 2xx
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print(f"[post_to_backend] HTTP error: {e}")
                    print(f"[post_to_backend] Status code: {response.status_code}")
                    try:
                        print(f"[post_to_backend] Response body: {response.text}")
                    except Exception:
                        pass
                    last_error = e
                    raise  # bubble out to outer except

                filename = response.headers.get(
                    'Content-Disposition',
                    'images.zip'
                ).split('filename=')[-1].strip('"')

                zip_path = os.path.join(OUTPUT_DIR, filename)

                with open(zip_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            # Validate the zip we just wrote
            if is_valid_zip(zip_path):
                extraction_path = []
                extraction_path.append(OUTPUT_DIR)
                if state['workflow']['organize_outputs_by_date']:
                    date_folder = datetime.now().strftime("%Y-%m-%d")
                    extraction_path.append(date_folder)
                if state['workflow']['organize_outputs_by_name']:
                    request_folder = state['workflow']['folder_name']
                    if request_folder.strip() == "":
                        request_folder = "Unnamed Set"
                    extraction_path.append(request_folder)
                if state['workflow']['organize_outputs_by_character']:
                    character_name = state['character_1']['character']
                    extraction_path.append(character_name)
                final_path = os.path.join(*extraction_path)
                os.makedirs(final_path, exist_ok=True)

                file_path = extract_zip(zip_path, final_path)
                success = True
            else:
                print(f"[post_to_backend] Downloaded file is not a valid zip: {zip_path}")
                print(f"[post_to_backend] Content-Type: {response.headers.get('Content-Type')}")
                last_error = RuntimeError("Downloaded file is not a valid zip")
                retries += 1
                time.sleep(RETRY_DELAY)

        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
            retries += 1
            last_error = e
            print(f"[post_to_backend] Timeout on attempt {retries}/{MAX_RETRIES}: {e}")
            time.sleep(RETRY_DELAY)

        except requests.exceptions.RequestException as e:
            retries += 1
            last_error = e
            print(f"[post_to_backend] Request error on attempt {retries}/{MAX_RETRIES}: {e}")
            time.sleep(RETRY_DELAY)

    if not success:
        print("[post_to_backend] All retries failed.")
        if last_error:
            print(f"[post_to_backend] Last error was: {repr(last_error)}")
        # unlock / reset UI
        completion_signaler.complete_signal.emit()
        return None

    return file_path


def is_valid_zip(file_path):
    """Checks if a file is a valid ZIP file."""
    return zipfile.is_zipfile(file_path)

def generate_unique_filename(original_name):
    """Generates a unique filename for extracted files."""
    _, ext = os.path.splitext(original_name)
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"image_{timestamp}_{unique_id}{ext}"

def extract_zip(zip_path, extraction_path):
    """
    Extracts a ZIP file and assigns unique filenames to contents.
    Updates the global most_recent_image with the final extracted file path.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if not file.endswith('/'):
                with zip_ref.open(file) as extracted_file:
                    file_data = extracted_file.read()
                    unique_name = generate_unique_filename(file)
                    extracted_file_path = os.path.join(extraction_path, unique_name)
                    with open(extracted_file_path, "wb") as img_file:
                        img_file.write(file_data)
                    # Overwrite so that after the loop, most_recent_image is the last file
                    return extracted_file_path
                    




