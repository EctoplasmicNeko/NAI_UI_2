import json
from PySide6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from ui.columns.notebooks.character_notebook_tabs.character_fluff_tab import CharacterFluffTab
from ui.columns.notebooks.character_notebook_tabs.SpeciesBar import SpeciesBar
from signaling.character_changed_signal import character_changed_signal
from signaling.refresh_character_lists import refresh_character_lists_signal
from signaling.cycle_character import cycle_character_signal
from data.datahub import get_all_characters
import random

class CharacterMiddleMasterTab(QFrame):

    def __init__(self, parent, image_cache, ID):
        super().__init__(parent)
        self.characters = get_all_characters()
        self.character_list = [char['nameID'] for char in self.characters]
        self.image_cache = image_cache
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        self.ID = ID
        self.build_character_master_tab()
        self.on_character_change()
        cycle_character_signal.character_cycle_signal.connect(self.handle_character_cycle)

    def build_character_master_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 1)

        self.fluff_tab = CharacterFluffTab(self, self.image_cache)
        self.grid.addWidget(self.fluff_tab, 0, 0)
        self.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.on_character_change())

        self.species_bar = SpeciesBar(self, self.image_cache)
        self.grid.addWidget(self.species_bar, 1, 0)

    def on_character_change(self):
        current_character = self.fluff_tab.character_select_combobox.currentText()
        if current_character != 'None':
            for character in self.characters:  # <-- loop over the dicts
                if character.get("nameID") == current_character:

                    gender = character.get("gender") or ""
                    species = character.get("species icon") or ""
                    quotes = character.get("quotes") or []

                    self.fluff_tab.character_fluff_fullname_label.setText(f'Full Name: {character.get("full_name")}')
                    self.fluff_tab.character_fluff_age_label.setText(f'Age: {character.get("age")} years old')
                    self.fluff_tab.character_fluff_species_label.setText(f'Species: {character.get("species")}')
                    self.fluff_tab.character_fluff_subspecies_label.setText(f'Subspecies: {character.get("subspecies")}')

                    if gender == "Male":
                        html = 'Gender: <span style="background:#123a6a; color:white; padding:2px 6px; border-radius:6px;">&nbsp;♂ Male &nbsp; </span>'
                    elif gender == "Female":
                        html = 'Gender: <span style="background:#b21f5b; color:white; padding:2px 6px; border-radius:6px;">&nbsp;♀ Female &nbsp;</span>'
                    elif gender == "Other":
                        html = 'Gender: <span style="background:#5a2a5a; color:white; padding:2px 6px; border-radius:6px;">&nbsp;⚥ Other&nbsp;</span>'
                    else:
                        html = 'Gender: <span style="background:#333333; color:white; padding:2px 6px; border-radius:6px;">&nbsp;? Other&nbsp;</span>'

                    self.fluff_tab.character_fluff_gender_label.setText(html)

                    species_to_id = {"human":0, "cat":1, "dog":2, "fox":3, "rabbit":4, "squirrel":5, "angel":6, "demon":7}
                    wanted_id = species_to_id.get(species.lower(), None)
                    if wanted_id is not None:
                        btn = self.species_bar.button_group.button(wanted_id)
                        if btn:
                            btn.setChecked(True)  # this will also emit your signal

                    if len(quotes) > 0:
                        selected_quote = random.choice(quotes)
                        html = f'<span style="color:white; border:1px solid rgba(255,255,255,0.4); padding:2px 6px; border-radius:6px;"><i>"{selected_quote}"</i></span>'
                        self.fluff_tab.character_fluff_quote_label.setText(html)
                    else:
                         self.fluff_tab.character_fluff_quote_label.clear()

                    try:
                        portrait_path = self.image_cache['portraits'][current_character.lower()]
                    except:
                        portrait_path = self.image_cache['images']['character_portraits']['fluff_placeholder']
                        
                    self.fluff_tab.update_portrait(portrait_path)

                    break

        else:
            self.fluff_tab.character_fluff_fullname_label.setText("Full Name: ???")
            self.fluff_tab.character_fluff_age_label.setText("Age: ???")
            self.fluff_tab.character_fluff_species_label.setText("Species: ???")
            self.fluff_tab.character_fluff_subspecies_label.setText("Subspecies: ???")

            self.fluff_tab.character_fluff_quote_label.clear()

            html = 'Gender: <span style="background:#333333; color:white; padding:2px 6px; border-radius:6px;">&nbsp;? Other&nbsp;</span>'
            self.fluff_tab.character_fluff_gender_label.setText(html)
            portrait_path = self.image_cache['images']['character_portraits']['fluff_placeholder']
            self.fluff_tab.update_portrait(portrait_path)
            group = self.species_bar.button_group

            # temporarily disable exclusivity so we can clear everything
            group.setExclusive(False)
            for button in group.buttons():
                button.setChecked(False)
            group.setExclusive(True)

        character_changed_signal.character_changed_signal.emit(self.ID, current_character)
        


    def export_state(self):
        current_character = self.fluff_tab.character_select_combobox.currentText()
        return {
        'character': current_character,
        }

    def import_state(self, loaded):
        loaded_character = loaded['character']
        print(f'loaded_character = {loaded_character}')
        if loaded_character == 'Loaded' or loaded_character not in self.character_list: #character association screen will launch here
            self.fluff_tab.character_select_combobox.setCurrentIndex(0) #sets to None
        else:
            self.fluff_tab.character_select_combobox.setCurrentText(loaded_character) #adds character and triggers index change, auto-fires On_Character_Change
    
    def handle_character_cycle(self, character_name, ID):
        if ID != self.ID:
            return  # Not for this tab
        if character_name in self.character_list:
            self.fluff_tab.character_select_combobox.setCurrentText(character_name)

    def on_refresh_character_list(self):
        current_character = self.fluff_tab.character_select_combobox.currentText()
        self.fluff_tab.character_select_combobox.blockSignals(True)
        self.fluff_tab.character_select_combobox.clear()
        self.fluff_tab.character_select_combobox.addItem('None')
        self.fluff_tab.character_select_combobox.addItems(self.character_list)
        self.fluff_tab.character_select_combobox.blockSignals(False)
        if current_character in self.character_list:
            self.fluff_tab.character_select_combobox.setCurrentText(current_character)
        else:
            self.fluff_tab.character_select_combobox.setCurrentText('None')


        
