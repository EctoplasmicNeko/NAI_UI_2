import random
from process.base64 import padded_image_to_b64
from process.metadata import prepare_metadata

def prepare_generate_payload(state):
    version = state['generate']['payload_type']
    if version == 'v3':
        payload, metadata = prepare_v3_payload(state, version)

    elif version == 'v4':
       payload, metadata = prepare_v4_payload(state, version)
        
    elif version == 'v45':
        payload, metadata = prepare_v45_payload(state, version)

    return payload, metadata


def prepare_v3_payload(state, version):

    positive_prompt = prepare_positive_prompt(state, version)
    negative_prompt = prepare_negative_prompt(state, version)
    brownian = prepare_brownian(state)
    seed = generate_seed(state)
    cfg = prepare_cfg(state)
    payload = {
    "action": "generate",
    "input": positive_prompt, #string
    "model": state['generate']['payload_name'],# string
    "parameters": {
        "add_original_image": True, #bool
        "cfg_rescale": state['generate']['rescale'], #number
        "controlnet_strength": 1,
        "dynamic_thresholding": state['generate']['decrisp'], #bool
        "height": state['generate']['image_height'], #int
        "legacy_v3_extend": state['generate']['legacy_v3'], #bool
        "n_samples": 1,
        "negative_prompt": negative_prompt, #string
        "noise_schedule": state['generate']['schedule'], #string
        "sampler": state['generate']['sampler'], #string
        "scale": state['generate']['scale'], #number
        "seed": seed, #int
        "sm": state['generate']['SMEA'], #bool
        "sm_dyn": state['generate']['DYN'], #bool
        "steps": state['generate']['steps'], #number
        "width": state['generate']['image_width'], #int
        "skip_cfg_above_sigma":cfg, #number
        "deliberate_euler_ancestral_bug": brownian[1],
        "prefer_brownian": brownian[0]
    }
}
    metadata = prepare_metadata(state, payload)
    return payload, metadata

def prepare_v4_payload(state, version):
        
    positive_prompt = prepare_positive_prompt(state, version)
    negative_prompt = prepare_negative_prompt(state, version)
    positive_character_captions = prepare_positive_character_prompt(state)
    negative_character_captions = prepare_negative_character_prompt(state)
    seed = generate_seed(state)
    cfg = prepare_cfg(state)
    brownian = prepare_brownian(state)

    payload = {
    "action": "generate",
    "input": positive_prompt,
    "model": state['generate']['payload_name'],
    "parameters": {
        "add_original_image": True,
        "cfg_rescale": state['generate']['rescale'],
        "legacy_uc": state['generate']['legacy_v4'],
        "controlnet_strength": 1,
        "deliberate_euler_ancestral_bug": brownian[1],
        "prefer_brownian": brownian[0],
        "dynamic_thresholding": False, #can v4 use this? its in the payload but theres no toggle. Set to false for now. It can, the effect seems minor.
        "height": state['generate']['image_height'],
        "width": state['generate']['image_width'],
        "n_samples": 1,
        "negative_prompt": negative_prompt,
        "noise_schedule": state['generate']['schedule'],
        "sampler": state['generate']['sampler'],
        "scale": state['generate']['scale'],
        "seed": seed,
        "skip_cfg_above_sigma": cfg,
        "steps": state['generate']['steps'],
        "use_coords": True,
        "v4_negative_prompt": {
            "caption": {
                "base_caption": negative_prompt,
                "char_captions": negative_character_captions
            },
            "legacy_uc": state['generate']['legacy_v4']
        },
        "v4_prompt": {
            "caption": {
                "base_caption": positive_prompt,
                "char_captions": positive_character_captions
            },
            "use_coords": False,
            "use_order": True # if one of these is true, the negative version will be false. AI choice = coords false, order true. Non AI Choice = Both true.
        },
    }
}
    metadata = prepare_metadata(state, payload)
    return payload, metadata

def prepare_v45_payload(state, version):
        
    positive_prompt = prepare_positive_prompt(state, version)
    negative_prompt = prepare_negative_prompt(state, version)
    positive_character_captions = prepare_positive_character_prompt(state)
    negative_character_captions = prepare_negative_character_prompt(state)
    seed = generate_seed(state)
    cfg = prepare_cfg(state)
    brownian = prepare_brownian(state)
    

    if state['character_1']['character_reference_enabled'] and state['character_1']['character_reference_path'] != None:

        referenceb64 = padded_image_to_b64(state['character_1']['character_reference_path'])
        fidelity = float(state['character_1']['character_reference_fidelity'])
        styleaware = state['character_1']['character_reference_style_aware']
        refstrength = state['character_1']['character_reference_strength']
        
        payload = {
        "action": "generate",
        "input": positive_prompt, 
        "model": state['generate']['payload_name'],
        "parameters": {
            "add_original_image": True,
            "cfg_rescale": state['generate']['rescale'],
            "controlnet_strength": 1,
            "deliberate_euler_ancestral_bug": brownian[1],
            "prefer_brownian": brownian[0],
            "dynamic_thresholding": False, 
            "height": state['generate']['image_height'],
            "width": state['generate']['image_width'],
            "n_samples": 1,
            "negative_prompt": negative_prompt,
            "noise_schedule": state['generate']['schedule'],
            "sampler": state['generate']['sampler'],
            "scale": state['generate']['scale'],
            "seed": seed,
            "skip_cfg_above_sigma": cfg,
            "steps": state['generate']['steps'],
            "use_coords": True,
            "v4_negative_prompt": {
                "caption": {
                    "base_caption": negative_prompt,
                    "char_captions": negative_character_captions
                }
            },
            "v4_prompt": {
                "caption": {
                    "base_caption": positive_prompt,
                    "char_captions": positive_character_captions
                },
                "use_coords": False,
                "use_order": True # if one of these is true, the negative version will be false. AI choice = coords false, order true. Non AI Choice = Both true.
            },
            
        "director_reference_descriptions": [{
            "caption": {
                "base_caption": styleaware,
                "char_captions": []
            },
            "legacy_uc": False
        }],
        "director_reference_images": [referenceb64],  # raw base64, PNG preferred
        "director_reference_information_extracted": [1], #must be 1 or will return 500 error
        "director_reference_secondary_strength_values": [fidelity], #this value is tied to fidelity, range 0-1 float
        "director_reference_strength_values": [refstrength] #Defraults to 1 on the website, can be any value
            
        }
    }
        
        metadata = prepare_metadata(state, payload)
        return payload, metadata

        
    else:
        payload = {
        "action": "generate",
        "input": positive_prompt, 
        "model": state['generate']['payload_name'],
        "parameters": {
            "add_original_image": True,
            "cfg_rescale": state['generate']['rescale'],
            "controlnet_strength": 1,
            "deliberate_euler_ancestral_bug": brownian[1],
            "prefer_brownian": brownian[0],
            "dynamic_thresholding": False, 
            "height": state['generate']['image_height'],
            "width": state['generate']['image_width'],
            "n_samples": 1,
            "negative_prompt": negative_prompt,
            "noise_schedule": state['generate']['schedule'],
            "sampler": state['generate']['sampler'],
            "scale": state['generate']['scale'],
            "seed": seed,
            "skip_cfg_above_sigma": cfg,
            "steps": state['generate']['steps'],
            "use_coords": True,
            "v4_negative_prompt": {
                "caption": {
                    "base_caption": negative_prompt,
                    "char_captions": negative_character_captions
                }
            },
            "v4_prompt": {
                "caption": {
                    "base_caption": positive_prompt,
                    "char_captions": positive_character_captions
                },
                "use_coords": False,
                "use_order": True # if one of these is true, the negative version will be false. AI choice = coords false, order true. Non AI Choice = Both true.
            },
        }
    }
        

        metadata = prepare_metadata(state, payload)
        return payload, metadata



def prepare_positive_prompt(state, version):
    prompt = []
    preset =  state['global_prompt']['global_positive_preset_tags']
    target =  state['global_prompt']['global_positive_preset_target']
    character_count = state['global_prompt']['character_number']

    global_positive_prompt = state['global_prompt']['global_positive_prompt']
    if global_positive_prompt != "" and global_positive_prompt != None:
        split_global_positive = global_positive_prompt.split(",")
        prompt.extend(split_global_positive)
        print(f"Global Positive Prompt: {global_positive_prompt}")
    else:
        print("No Global Positive Prompt found.")
    
    
    if character_count > 0:
        for index in range(1, character_count + 1):
            preset_global_positive = state[f'character_{index}']['character_preset_global_positive']
            if preset_global_positive != '' and preset_global_positive != None:
                split_preset_global_positive = preset_global_positive.split(",")
                prompt.extend(split_preset_global_positive)
                print(f"Appending character {index} global positive preset: {preset_global_positive}")
            else:
                print(f"No global positive preset found for character {index}.")

            if version == 'v3':

                for qw in state[f'character_{index}']['character_positive_quick_weights']:
                    prompt.append(qw)

                preset_positive = state[f'character_{index}']['character_preset_positive']
                if preset_positive != None and preset_positive != "":
                    split_preset_positive = preset_positive.split(",")
                    prompt.extend(split_preset_positive)

                prompt_positive = state[f'character_{index}']['character_positive_prompt']
                if prompt_positive != "" and prompt_positive != None:
                    split_prompt_positive = prompt_positive.split(",")
                    prompt.extend(split_prompt_positive)

    print(f"Global Positive Preset: {preset}")
    if preset != '' and preset != None:
        if target == 'end':
            split_preset = preset.split(",")
            prompt.extend(split_preset)
            print(f"Appended preset at end: {preset}")
        elif target == 'start':
            split_preset = preset.split(",")
            for item in reversed(split_preset):
                prompt.insert(0, item)
            print(f"Inserted preset at start: {preset}")
    else:
        print("No global positive preset found.")

    final_prompt = ", ".join(prompt)
    return final_prompt

def prepare_negative_prompt(state, version):
    prompt = []
    preset = state['global_prompt']['global_negative_preset_tags']
    character_count = state['global_prompt']['character_number']

    global_negative_prompt = state['global_prompt']['global_negative_prompt']
    if global_negative_prompt != "" and global_negative_prompt != None:
        split_global_negative = global_negative_prompt.split(",")
        prompt.extend(split_global_negative)
    
    if character_count > 0:
        for index in range(1, character_count + 1):
            preset_global_negative = state[f'character_{index}']['character_preset_global_negative']
            if preset_global_negative != None and preset_global_negative != '':
                split_preset_global_negative = preset_global_negative.split(",")
                prompt.extend(split_preset_global_negative)

            if version == 'v3':
                    
                    for qw in state[f'character_{index}']['character_negative_quick_weights']:
                        prompt.append(qw)

                    preset_negative = state[f'character_{index}']['character_preset_negative']
                    if preset_negative != None and preset_negative != "":
                        split_preset_negative = preset_negative.split(",")
                        prompt.extend(split_preset_negative)

                    prompt_negative = state[f'character_{index}']['character_negative_prompt']
                    if prompt_negative != "" and prompt_negative != None:
                        split_prompt_negative = prompt_negative.split(",")
                        prompt.extend(split_prompt_negative)
    
    if preset != None and preset != '':
        prompt.append(preset)
    final_prompt = ", ".join(prompt)
    return final_prompt

def prepare_positive_character_prompt(state):
    character_captions = []
    character_count = state['global_prompt']['character_number']

    for id in range(1, character_count + 1):
        if id <= character_count:
            key = f"character_{id}"

            caption = []

            for weight in state[key]['character_positive_quick_weights']:
                caption.append(weight)

            preset_positive = state[key]['character_preset_positive']
            if preset_positive != None and preset_positive != "":
                split_preset_positive = preset_positive.split(",")
                caption.extend(split_preset_positive)

            outfit_positive = state[key]['character_outfit_preset_positive']
            if outfit_positive != None and outfit_positive != "":
                split_outfit_positive = outfit_positive.split(",")
                caption.extend(split_outfit_positive)

            prompt_positive = state[key]['character_positive_prompt']
            if prompt_positive != None and prompt_positive != "":
                split_prompt_positive = prompt_positive.split(",")
                caption.extend(split_prompt_positive)

            print(f"Preparing associations for character {id} with caption: {caption}")
            for tag in caption:
                tag = tag.strip()
            print(f"Cleaned caption for character {id}: {caption}")

            caption_set = set(caption)
            associations_to_add = []

            associations_positive = state[key]['character_tag_associations']

            for association in associations_positive:

                blacklist = association.get('blacklist')
                blacklist_found = False
                print(f"blacklist: {blacklist}")
                if blacklist:
                    for blacklist_tag in blacklist:
                        if blacklist_tag in caption_set:
                            blacklist_found = True
                            break
                if blacklist_found:
                    continue

                trigger_tags = []
                raw_triggers = association['trigger']

                for raw_trigger in raw_triggers:
                    trigger = str(raw_trigger).strip()
                    if trigger:
                        trigger_tags.append(trigger)

                trigger_found = False
                for trigger_tag in trigger_tags:
                    if trigger_tag in caption_set:
                        trigger_found = True
                        break

                if not trigger_found:
                    continue

                cleaned_inject_tags = []
                raw_inject_tags = association['inject']

                for raw_tag in raw_inject_tags:
                    tag = str(raw_tag).strip()
                    if tag:
                        cleaned_inject_tags.append(tag)

                for inject_tag in cleaned_inject_tags:
                    if inject_tag in caption_set:
                        continue
                    if inject_tag in associations_to_add:
                        continue

                    associations_to_add.append(inject_tag)
                    caption_set.add(inject_tag)

            caption.extend(associations_to_add)
            print(f"Final caption for character {id}: {caption}")

            joined_caption = ", ".join(caption)

            print(f"Final cleaned caption for character {id}: {joined_caption}")

            payload = {
                "centers": [
                    {
                        "x": state[key]['character_x_coordinate'],
                        "y": state[key]['character_y_coordinate']
                    }
                ],
                "char_caption": joined_caption
            }
            character_captions.append(payload)
    return character_captions

def prepare_negative_character_prompt(state):
    character_captions = []
    character_count = state['global_prompt']['character_number']

    for id in range(1, character_count + 1):
        if id <= character_count:
            key = f"character_{id}"

            caption = []

            for weight in state[key]['character_negative_quick_weights']:
                caption.append(weight)

            preset_negative = state[key]['character_preset_negative']
            if preset_negative != None and preset_negative != "":
                split_preset_negative = preset_negative.split(",")
                caption.extend(split_preset_negative)

            outfit_negative = state[key]['character_outfit_preset_negative']
            if outfit_negative != None and outfit_negative != "":
                split_outfit_negative = outfit_negative.split(",")
                caption.extend(split_outfit_negative)

            prompt_negative = state[key]['character_negative_prompt']
            if prompt_negative != "" and prompt_negative != None:
                split_prompt_negative = prompt_negative.split(",")
                caption.extend(split_prompt_negative)   

            print(f"Preparing negative associations for character {id} with caption: {caption}")
            caption = [tag.strip() for tag in caption]    

            print(f"Cleaned negative caption for character {id}: {caption}")
            joined_caption = ", ".join(caption)
            
            payload = {
                "centers": [
                    {
                        "x": state[key]['character_x_coordinate'],
                        "y": state[key]['character_y_coordinate']
                    }
                ],
                "char_caption": joined_caption
            }
            character_captions.append(payload)
    return character_captions

def generate_seed(state):
    state_seed = state['generate']['seed']
    if state_seed > 0:
        return state_seed
    else:
        random_seed = random.randint(1, 4294967295)
        return random_seed
    
def prepare_cfg(state):
    if state['generate']['variety+']:
        return state['generate']['variety+_value']
    else:
        state_cfg = state['generate']['cfg']
        if state_cfg >= 0:
            return state_cfg
        else:
            return None
        
def prepare_brownian(state):
    if state['generate']['brownian']:
        return (True, False)
    else:
        return (False, True)
    


    

    