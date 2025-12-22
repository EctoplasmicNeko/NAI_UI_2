import json
from PySide6.QtWidgets import QGridLayout, QFrame, QDoubleSpinBox
from ui.columns.notebooks.character_sub_notebook import CharacterSubNotebook
from signaling.character_changed_signal import character_changed_signal
from signaling.outfit_changed import outfit_changed_signal
from data.paths import CONFIG_DIR
from process.character_autocycle_manager import CharacterAutoCycleManager
from data.datahub import get_all_characters

class CharacterLowerMasterTab(QFrame):

    def __init__(self, parent, image_cache, ID):
        super().__init__(parent)
        self.current_character = 'None'
        self.ID = ID
        self.image_cache = image_cache
        self.build_character_master_tab()
        character_changed_signal.character_changed_signal.connect(self.on_character_change)
        self.character_autocycle_manager = CharacterAutoCycleManager(self, self.current_character)
              
    def build_character_master_tab(self):

        self.characters = get_all_characters()                

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.sub_notebook = CharacterSubNotebook(self,self.image_cache, self.ID)
        self.grid.addWidget(self.sub_notebook, 0, 0)

        self.sub_notebook.character_sub_tab_1.quick_weights_tab.quickWeightsChanged.connect(
            self.on_quick_weights_changed
)
        outfit_changed_signal.outfit_changed.connect(
            self.on_outfit_preset_changed
        )

    def on_character_change(self, ID, current_character):
        if ID != self.ID:
            return  # Not for this tab
        self.current_character = current_character

        if current_character != 'None':
            for character in self.characters:  # <-- loop over the dicts
                if character.get("nameID") == current_character:

                    self.sub_notebook.character_sub_tab_3.rebuild_character_references(current_character.lower())

                    character_positive_prompt = []
                    for tag in character['c_positive']:
                        cleaned_cpos_tag = tag['tag'].strip()
                        if tag['strength'] == 1.0:
                            character_positive_prompt.append(tag['tag'])
                        else:
                            character_positive_prompt.append(f"{tag['strength']:.1f}::{cleaned_cpos_tag}::")

                    self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_character_textbox.setText(", ".join(character_positive_prompt))

                    character_negative_prompt = []
                    for tag in character['c_negative']:
                        cleaned_cneg_tag = tag['tag'].strip()
                        if tag['strength'] == 1.0:
                            character_negative_prompt.append(tag['tag'])
                        else:
                            character_negative_prompt.append(f"{tag['strength']:.1f}::{cleaned_cneg_tag}::")

                    self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_character_textbox.setText(", ".join(character_negative_prompt))

                    character_positive_global = []
                    for tag in character['g_positive']:
                        cleaned_gpos_tag = tag['tag'].strip()
                        if tag['strength'] == 1.0:
                            character_positive_global.append(tag['tag'])
                        else:
                            character_positive_global.append(f"{tag['strength']:.1f}::{cleaned_gpos_tag}::")

                    self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_global_textbox.setText(", ".join(character_positive_global))

                    character_negative_global = []
                    for tag in character['g_negative']:
                        cleaned_gneg_tag = tag['tag'].strip()
                        if tag['strength'] == 1.0:
                            character_negative_global.append(tag['tag'])
                        else:
                            character_negative_global.append(f"{tag['strength']:.1f}::{cleaned_gneg_tag}::")

                    self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_global_textbox.setText(", ".join(character_negative_global))

                    self.sub_notebook.character_sub_tab_1.quick_weights_tab.rebuild_quick_weights(
                        current_character,
                        character.get("quick_weights") or []
                    )
                    
                    self.sub_notebook.character_sub_tab_5.outfit_combo.blockSignals(True)
                    self.sub_notebook.character_sub_tab_5.outfit_combo.clear()
                    self.sub_notebook.character_sub_tab_5.outfit_combo.addItems(["None"] + [outfit['name'] for outfit in character['outfits']])
                    self.sub_notebook.character_sub_tab_5.outfit_combo.blockSignals(False)
                    self.sub_notebook.character_sub_tab_5.outfit_combo.setCurrentText(character['most_recent_outfit'])
                
                    self.setProperty('tag_associations', character.get("tag_associations") or [])
                    break


        else:

            self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_character_textbox.clear()
            self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_character_textbox.clear()
            self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_global_textbox.clear()
            self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_global_textbox.clear()
            self.sub_notebook.character_sub_tab_5.outfit_combo.clear()
            self.sub_notebook.character_sub_tab_5.outfit_combo.addItem("None")
            self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.clear()
            self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.clear()

            self.sub_notebook.character_sub_tab_1.quick_weights_tab.rebuild_quick_weights(None, [])
            self.sub_notebook.character_sub_tab_3.rebuild_character_references(None)


    def export_state(self):

        button = self.sub_notebook.character_sub_tab_2.coordinate_button_group.checkedButton()
        button_id = self.sub_notebook.character_sub_tab_2.coordinate_button_group.checkedId()
        if button is None:
            y_coordinate = None
            x_coordinate = None
        else:
            y_coordinate, x_coordinate = button.property('coordinates')

        positive_quick_weights = []
        negative_quick_weights = []

        for widget in self.sub_notebook.character_sub_tab_1.quick_weights_tab.findChildren(QDoubleSpinBox):
            value = widget.value()
            if value != 0:
                tag = widget.property('tag')
                value_str = f"{value:.1f}" #gets rid of trailing fraction and keeps number to one decimal point
                merged = f"{value_str}::{tag}::"
                is_negative = widget.property('negative')
                if is_negative:
                    negative_quick_weights.append(merged)
                else:
                    positive_quick_weights.append(merged)

        active_reference = None
        if self.current_character != 'None':
            btn = self.sub_notebook.character_sub_tab_3.reference_button_group.checkedButton()
            if btn is not None:
                active_reference = btn.property('image_path')
                print(f'active_reference = {active_reference}')
        
        fidelity = self.sub_notebook.character_sub_tab_3.fidelity_spinner.value()
        fidelity = f"{fidelity:.2f}"
        fidelity = float(fidelity)
        overall_fidelity = 1.00 - fidelity #for whatever reason, NAI uses inverse fidelity for this parameter
        
        reference_strength = self.sub_notebook.character_sub_tab_3.refstrength_spinner.value()
        reference_strength = f"{reference_strength:.2f}"
        reference_strength = float(reference_strength)
        
        if self.sub_notebook.character_sub_tab_3.style_aware_checkbox.isChecked():
            styleaware = 'character&style'
        else:
            styleaware = 'character'
        
        

        return {
        'character_positive_prompt': self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_textbox.toPlainText(), #generation
        'character_negative_prompt': self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_textbox.toPlainText(), #generation
        'character_coordinate_button': button_id, #save/load
        'character_y_coordinate': y_coordinate, #generation
        'character_x_coordinate': x_coordinate, #generation
        'character_positive_quick_weights': positive_quick_weights, #generation
        'character_negative_quick_weights': negative_quick_weights, #generation
        'character_preset_positive': self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_character_textbox.toPlainText(),
        'character_preset_negative': self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_character_textbox.toPlainText(),
        'character_preset_global_positive': self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_global_textbox.toPlainText(),
        'character_preset_global_negative': self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_global_textbox.toPlainText(),
        'character_outfit_preset_positive': self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.toPlainText(),
        'character_outfit_preset_negative': self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.toPlainText(),
        'most_recent_outfit': self.sub_notebook.character_sub_tab_5.outfit_combo.currentText(),
        'character_reference_path': active_reference,
        'character_reference_enabled': self.sub_notebook.character_sub_tab_3.enable_reference_checkbox.isChecked(),
        'character_reference_style_aware': styleaware,
        'character_reference_fidelity': overall_fidelity,
        'character_reference_strength': reference_strength,
        'character_tag_associations': self.property('tag_associations') if self.current_character != 'None' else []
        }
        
    def import_state(self, loaded):
        loaded_character = loaded['character']
        print(f'loaded_character = {loaded_character}')

        saved_id = loaded['character_coordinate_button'] 
        if saved_id != -1:
            button = self.sub_notebook.character_sub_tab_2.coordinate_button_group.button(saved_id)
            button.setChecked(True)
            button.click() 

        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_textbox.setText(loaded['character_positive_prompt'])
        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_textbox.setText(loaded['character_negative_prompt'])

        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_character_textbox.setText(loaded['character_preset_positive'])
        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_character_textbox.setText(loaded['character_preset_negative'])

        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_global_textbox.setText(loaded['character_preset_global_positive'])
        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_global_textbox.setText(loaded['character_preset_global_negative'])

        self.sub_notebook.character_sub_tab_5.outfit_combo.setCurrentText(loaded['most_recent_outfit'])

        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.setText(loaded['character_outfit_preset_positive'])
        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.setText(loaded['character_outfit_preset_negative'])

    
    def on_quick_weights_changed(self, character_name, quick_weights_data):
        """Called whenever a quick weight spinner is changed."""

        # update in-memory characters list
        changed = False
        for character in self.characters:
            if character.get("nameID") == character_name:
                character["quick_weights"] = quick_weights_data
                changed = True
                break

        if not changed:
            return  # character not found, nothing to save

        # write back to characters.json
        characters_file_path = CONFIG_DIR / "characters.json"
        with characters_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.characters, f, indent=2, ensure_ascii=False)

    def on_outfit_preset_changed(self, new_outfit_name, ID):
        """Update the currently selected character's most recent outfit and save."""

        if ID != self.ID:
            return  # Not for this tab

        if self.current_character == "None":
            self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.clear()
            self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.clear()
            return
        else:
            for character in self.characters:  # <-- loop over the dicts
                if character.get("nameID") == self.current_character:
                    # Find the outfit details
                    outfit_details = next((outfit for outfit in character['outfits'] if outfit['name'] == new_outfit_name), None)
                    if outfit_details:
                        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.setText(outfit_details.get('o_positive', ''))
                        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.setText(outfit_details.get('o_negative', ''))
                    else:
                        self.sub_notebook.character_sub_tab_1.prompt_tab.positive_prompt_outfit_textbox.clear()
                        self.sub_notebook.character_sub_tab_1.prompt_tab.negative_prompt_outfit_textbox.clear()
                    break

        changed = False

        for character in self.characters:
            if character.get("nameID") == self.current_character:
                character["most_recent_outfit"] = new_outfit_name
                changed = True
                break

        if not changed:
            return

        # Write characters.json
        characters_file_path = CONFIG_DIR / "characters.json"
        with characters_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.characters, f, indent=2, ensure_ascii=False)

        print(f"[Character] Saved most_recent_outfit: {new_outfit_name}")

    def on_refresh_character_list(self):
        self.sub_notebook.character_sub_tab_4.reload_tags()
    
