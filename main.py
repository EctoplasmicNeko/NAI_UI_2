# main.py
from ui.ui_main import run_app
from data import datahub
from data.paths import (
    PORTRAITS_DIR,
    OUTPUT_DIR,
    CHARACTERS_DIR,
    REFERENCE_DIR
)
# data/paths.py
def ensure_dirs() -> None:
    PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHARACTERS_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)


# This check ensures we only run the window when executing directly
if __name__ == "__main__":
    ensure_dirs()
    datahub.load_all()
    datahub.load_characters()
    run_app()


#changelog:
#25/11/2025 - added metadata writing to generate process
#25/11/2025 - fixed issue with character quick weights + preset not being added to v3 prompts
#25/11/2025 - added check for None in positve/negative preset tags storage to remove extra commas
#25/11/2025 - added negative preset injection to global prompts (was missing)
#25/11/2025 - added character_global tag injection to global positive/negative (was missing)
#25/11/2025 - rewrote character prompt building to generate to account for v3 and empty values
#25/11/2025 - fixed bug causing character presets to not load correctly in manage characters window, causing them to be overwritten on close
#25/11/2025 - added brownian handling to v3 payload (was missing)
#26/11/2025 - fixed bug causing v4 legacy uc to not be passed to generate payload (was missing in parameters)
#26/11/2025 - added legacy_v4 to state gathering, renamed legacy to legacy_v3 for clarity
#26/11/2025 - added metadata gathering to v4 and v45 payload
#27/11/2025 - added import/export of legacy_v4 to UI state
#27/11/2025 - v4 now handles empty character prompts/presets correctly
#27/11/2025 - removed quick weight stacking, now generates page on character select
#27/11/2025 - added support for positive and negative quick weights separately
#27/11/2025 - fixed bug causing ghost windows on character reference tab when changing characters
#27/11/2025 - added custom min/max ranges to quick weights
#27/11/2025 - added placeholder when no quick weights are assigned to character
#27/11/2025 - quick weights now normalize one decimal place
#28/11/2025 - fixed legacy uc v4 parameter passing bug
#29/11/2025 - added character preset and global preset pages to character prompt tab, added prompt field switching, removed property storage of preset prompts
#29/11/2025 - restore from metadata function added
#29/11/2025 - image generate master tab now disables incompatible checkboxes when model is changed
#29/11/2025 - fixed bug causing workflow tab to duplicate tasks on import state
#29/11/2025 - added locking of generation window during active generation to prevent sending multiple requests
#29/11/2025 - added tabbed behavior to global prompt settings and adjusted state storage accordingly
#29/11/2025 - removed per-version prepare_metadata and restore_from_metadata functions, now a single function that handles all versions as changes to ui prompt handling make per-version functions redundant
#29/11/2025 - anlas warning correctly resets when steps below 29
#30/11/2025 - Window locking now uses signals, signal on failure to unlock window
#30/11/2025 - window locking now disables signals rather than disabling the whole window
#01/12/2025 - output directory now routes to correct OUTPUT_DIR variable
#01/12/2025 - Failed generation now correctly resets UI and unlocks window without passing invalid file paths
#01/12/2025 - adjusted start and complete signals to be emitted from main ui rather than process main execpt for on failure to prevent duplicate workers
#01/12/2025 - removed fruit salad, added theme support
#01/12/2025 - added theme loading to program settings tab
#01/12/2025 - added widget object names for theme application
#02/12/2025 - minimal character tab now hides fluff and portrait frames when toggled off
#02/12/2025 - species bar now hides when toggled off
#02/12/2025 - species bar now parents to character master tab
#02/12/2025 - added restore state from NAI native metadata format
#02/12/2025 - added fidelity parameter to director reference image handling (was set to 1.0 previously)
#02/12/2025 - fixed bug causing fidelity to be inverted (NAI uses 0=high fidelity, 1=low fidelity)
#02/12/2025 - fixed bug causing fidelity to be sent as ? a string rather than a float. Still don't know how its not a float when it gets to process_generate.
#02/12/2025 - v4.5 generations that use director reference images now capture b64 in metadata
#03/12/2025 - added b64 capture toggle to program settings
#03/12/2025 - added b64 capture state import/export to program settings
#03/12/2025 - negative global prompt builder now skips global quality preset if preset is empty
#04/12/2025 - fixed crash on loading v3 and sdxl images due to character count handling (was expecting char_captions key, now sets count to 0)
#04/12/2025 - fluff tab and character parameters are now seperate fields in UI, ui stretch updated accordingly
#04/12/2025 - character portaits can now be changed aftre creating a character
#04/12/2025 - image size presets are now properly detected on importing state from metadata
#05/12/2025 - character lists now correctly refresh when characters are added/removed
#05/12/2025 - image settings tab now has quick buttons to set seed to 0 and disable rescale and cfg
#05/12/2025 - added import options dialog on image drop with metadata
#05/12/2025 - import dialog now defaults checkboxes to previous import state
#07/12/2025 - added auto-cycling for characters
#08/12/2025 - added auto-random for characters
#08/12/2025 - character cycling now cycles only on generation task
#09/12/2025 - added manual values to loop control
#09/12/2025 - loops now divided into loop and sets
#09/12/2025 - added set start and complete signals to completion signaler
#09/12/2025 - added on set cycle trigger to character auto cycle manager
#09/12/2025 - fixed bug causing character cycle timing to be offset by one generation (resetting couter to 0 after incrimenting it)
#10/12/2025 - sets can now be set to 0 to use 'per character' mode, filters added to workflow tab

#10/12/2025 - 15/12/25
#Added outfit field to character data
#Updated character tabs to include outfit field
#character files now store to seperate json files rather than a single file
#Character files now store tokenized prompts
#updated prompt building to use tokenized prompts
#Consolidated character tab data reloading into single refresh signal on left column
#reconfigured file system to seperate user editable data from program data
#character manager now edits individual character files
#Added reference image folder and individual json deletion on character delete
#character manager now loads and saves tokenized prompts
#character manager now deconstucts weighted tags into compatible tokenized format
#Fixed bug causing character data to not reload correctly on character add/remove (now uses reload_character_data signal to reload cache)

#- version 0.1 released

#21/12/2025 - added basic functionality for hydrus sidecar writing
#22/12/2025 - save state now retains set, loop, delay and filter settings in workflow tab
#22/12/2025 - menu button groups now select first button by default on init
#22/12/2025 - added folder sorting to workflow tab
#22/12/2025 - implimented folder sorting in process main

#to do:

# add restore functionality to reference images metadata
# add character quick weight display to manage characters window
# replace character portrait label with toolbutton to lauch stats window
# add character stats window
# update metadata to process dict quick weights
# update image cache to store image and path for faster loading
# make state capture and restore reference tab state
# autocycle to start from selected character rather than always from first in list
# allow character editing after creation
# fix bugs related to collapsing character tabs 
# rewrite prompt generation logic to seperate list collation/spllitting from assembly to support additional functions (wildcars, full tag association)
#FINISH COORDINATE TAB FUNCTIONALITY





