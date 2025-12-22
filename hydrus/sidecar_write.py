
import os

def write_hydrus_sidecar(file_path, state):

    tags = get_tag_pairs(state)
    sidecar = file_path + ".txt"
    with open(sidecar, "w", encoding="utf-8") as f:
        f.write("\n".join(tags) + "\n")
    return (f"WROTE: {os.path.basename(sidecar)}", True)
    
def get_tag_pairs(state):
    tags = []

    for i in range(state['global_prompt']['character_number']):
        key = f'character_{i + 1}'
        character = state[key]['character']
        if character == 'None':
            character_name = 'character: Other'
        else:
            character_name = f'character: {character}'
        if character_name not in tags:
            tags.append(character_name)

    height = state['generate']['image_height']
    width = state['generate']['image_width']
    if height > width:
        tags.append('orientation: portrait')
    elif width > height:
        tags.append('orientation: landscape')
    else:
        tags.append('orientation: square')

    return tags

