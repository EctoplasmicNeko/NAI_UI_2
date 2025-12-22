from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QDialog, QGridLayout, QComboBox, QLineEdit, QTextEdit, QFrame, QFileDialog
from windows.error import Error
from windows.confirmation import Confirm
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from signaling.refresh_character_lists import refresh_character_lists_signal
import json
from pathlib import Path    
from shutil import copy2
import shutil
from data.datahub import get_all_characters
from data.paths import PORTRAITS_DIR, REFERENCE_DIR, CHARACTERS_DIR


class ManageCharacterWindow(QDialog):
    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.setWindowTitle("Manage Characters")
        self.image_cache = image_cache
        self.build_manage_character_window()
        self.on_character_change()
        self.characters_file_path = CHARACTERS_DIR
        self.portraits_dir = PORTRAITS_DIR

    def build_manage_character_window(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.characters = get_all_characters()
        self.character_list = [f'{character["nameID"]}' for character in self.characters]
        self.character_list.insert(0, 'New Character')

        self.button_frame = QFrame(self)
        self.grid.addWidget(self.button_frame, 0, 0, 1, 3)
        self.button_frame_grid = QGridLayout(self.button_frame)

        self.add_character_button = QPushButton('Add Character', self)
        self.add_character_button.clicked.connect(self.add_new_character)
        self.button_frame_grid.addWidget(self.add_character_button, 0, 0)

        self.delete_character_button = QPushButton('Delete Character', self)
        self.delete_character_button.clicked.connect(self.delete_character)
        self.button_frame_grid.addWidget(self.delete_character_button, 0, 1)

        self.copy_character_button = QPushButton('Copy Character', self)
        self.copy_character_button.clicked.connect(self.copy_character)
        self.button_frame_grid.addWidget(self.copy_character_button, 0, 2)       
        
        self.character_select_combobox = QComboBox(self)
        self.character_select_combobox.addItems(self.character_list)
        self.character_select_combobox.setEditable(False)
        self.character_select_combobox.currentIndexChanged.connect(self.on_character_change)
        self.grid.addWidget(self.character_select_combobox, 1, 0)


        self.character_id_label = QLabel("Character ID:", self)
        self.character_id_label.setTextFormat(Qt.RichText)
        self.character_id_label.setText('Character ID <span style="color:#ff5555;">(*)</span>')
        self.grid.addWidget(self.character_id_label, 2, 0)

        self.character_id_lineedit = QLineEdit(self)
        self.character_id_lineedit.setPlaceholderText("Character ID")
        self.character_id_lineedit.setToolTip("Unique identifier for the character, required)")
        self.grid.addWidget(self.character_id_lineedit, 2, 1)

        self.character_fullname_label = QLabel("Full Name:", self)
        self.character_fullname_label.setText('Full Name')
        self.grid.addWidget(self.character_fullname_label, 3, 0)    

        self.character_fullname_lineedit = QLineEdit(self)
        self.character_fullname_lineedit.setPlaceholderText("Full Name")
        self.character_fullname_lineedit.setToolTip("The character's full name (longer, more descriptive)")
        self.character_fullname_lineedit.editingFinished.connect(self.save_fullname)
        self.grid.addWidget(self.character_fullname_lineedit, 3, 1)

        self.character_age_label = QLabel("Age:", self)
        self.character_age_label.setText('Age') 
        self.grid.addWidget(self.character_age_label, 4, 0)

        self.character_age_lineedit = QLineEdit(self)
        self.character_age_lineedit.setPlaceholderText("Age")   
        self.character_age_lineedit.setToolTip("The character's age")
        self.character_age_lineedit.editingFinished.connect(self.save_age)
        self.grid.addWidget(self.character_age_lineedit, 4, 1)

        self.character_gender_label = QLabel("Gender:", self)   
        self.grid.addWidget(self.character_gender_label, 5, 0)

        self.character_gender_combobox = QComboBox(self)
        self.character_gender_combobox.setToolTip("The character's gender")
        self.character_gender_combobox.addItems(['none specified','Male', 'Female', 'Other'])
        self.character_gender_combobox.setEditable(False)           
        self.character_gender_combobox.setCurrentText('Gender')     
        self.character_gender_combobox.currentIndexChanged.connect(self.save_gender)
        self.grid.addWidget(self.character_gender_combobox, 5, 1)   

        self.character_species_label = QLabel("Species:", self)
        self.character_species_label.setText('Species')
        self.grid.addWidget(self.character_species_label, 6, 0)

        self.character_species_lineedit = QLineEdit(self)
        self.character_species_lineedit.setPlaceholderText("Species")
        self.character_species_lineedit.setToolTip("The character's species")
        self.character_species_lineedit.editingFinished.connect(self.save_species)
        self.grid.addWidget(self.character_species_lineedit, 6, 1)

        self.character_subspecies_label = QLabel("Subspecies:", self)
        self.character_subspecies_label.setText('Subspecies')
        self.grid.addWidget(self.character_subspecies_label, 7, 0)

        self.character_subspecies_lineedit = QLineEdit(self)
        self.character_subspecies_lineedit.setPlaceholderText("Subspecies")
        self.character_subspecies_lineedit.setToolTip("The character's subspecies")
        self.character_subspecies_lineedit.editingFinished.connect(self.save_subspecies)
        self.grid.addWidget(self.character_subspecies_lineedit, 7, 1)

        self.character_species_icon_label = QLabel("Species Icon:", self)
        self.character_species_icon_label.setText('Species Icon')
        self.grid.addWidget(self.character_species_icon_label, 8, 0)

        self.character_species_icon_combobox = QComboBox(self)
        self.character_species_icon_combobox.setToolTip("Icon representing the character's species")
        self.character_species_icon_combobox.addItems(['None', 'Human', 'Cat', 'Dog', 'Fox', 'Rabbit', 'Squirrel', 'Angel', 'Demon'])
        self.character_species_icon_combobox.setEditable(False)
        self.character_species_icon_combobox.setCurrentText('Species Icon')
        self.character_species_icon_combobox.currentIndexChanged.connect(self.save_species_icon)
        self.grid.addWidget(self.character_species_icon_combobox, 8, 1)

        self.character_c_positive_label = QLabel("Positive Character Prompt", self)
        self.character_c_positive_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_c_positive_label, 9, 0, 1, 3)

        self.character_c_positive_textedit = QTextEdit(self)
        self.character_c_positive_textedit.setPlaceholderText("Add to Positive Character Prompt:")
        self.character_c_positive_textedit.textChanged.connect(lambda: self.save_prompt_field("c_positive", self.character_c_positive_textedit))
        self.grid.addWidget(self.character_c_positive_textedit, 10, 0, 1, 3)

        self.character_c_negative_label = QLabel("Negative Character Prompt", self)
        self.character_c_negative_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_c_negative_label, 11, 0, 1, 3)

        self.character_c_negative_textedit = QTextEdit(self)
        self.character_c_negative_textedit.setPlaceholderText("Add to Negative Character Prompt:")
        self.character_c_negative_textedit.textChanged.connect(lambda: self.save_prompt_field("c_negative", self.character_c_negative_textedit))
        self.grid.addWidget(self.character_c_negative_textedit, 12, 0, 1, 3)

        self.character_g_positive_label = QLabel("Global Positive Prompt Additions:", self)
        self.character_g_positive_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_g_positive_label, 13, 0, 1, 3)

        self.character_g_positive_textedit =QTextEdit(self)
        self.character_g_positive_textedit.setPlaceholderText("Add to Positive Global Prompt")
        self.character_g_positive_textedit.textChanged.connect(lambda: self.save_prompt_field("g_positive", self.character_g_positive_textedit))
        self.grid.addWidget(self.character_g_positive_textedit, 14, 0, 1, 3)

        self.character_g_negative_label = QLabel("Global Negative Prompt Additions", self)
        self.character_g_negative_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_g_negative_label, 15, 0, 1, 3)   

        self.character_g_negative_textedit =QTextEdit(self)
        self.character_g_negative_textedit.setPlaceholderText("Add to Negative Global Prompt:")
        self.character_g_negative_textedit.textChanged.connect(lambda: self.save_prompt_field("g_negative", self.character_g_negative_textedit))
        self.grid.addWidget(self.character_g_negative_textedit, 16, 0, 1, 3)
        
        self.character_tags_label = QLabel("Tags", self)
        self.character_tags_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_tags_label, 17, 0, 1, 3)   

        self.character_tags_textedit =QTextEdit(self)
        self.character_tags_textedit.setPlaceholderText("Add to Tags:")
        self.character_tags_textedit.textChanged.connect(lambda: self.save_tags())
        self.grid.addWidget(self.character_tags_textedit, 18, 0, 1, 3)

        self.quick_weight_label = QLabel("Quick Weights", self)
        self.quick_weight_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.quick_weight_label, 19, 0, 1, 3)   

        self.quick_weight_textedit =QTextEdit(self)
        self.quick_weight_textedit.setPlaceholderText("Add to Quick Weights:")
        self.quick_weight_textedit.textChanged.connect(lambda: self.save_quick_weights())
        self.grid.addWidget(self.quick_weight_textedit, 20, 0, 1, 3)


        frame = QFrame(self)
        frame.setMinimumSize(170, 170)
        frame_grid = QVBoxLayout(frame)
        frame_grid.setContentsMargins(6, 6, 6, 6)
        frame_grid.setSpacing(4)

        self.grid.addWidget(frame, 2, 2, 6, 1)

        # === portrait label (keep as attribute!) ===
        self.portrait_label = QLabel(frame)
        self.portrait_label.setAlignment(Qt.AlignCenter)
        self.portrait_label.setFixedSize(150, 150)
        frame_grid.addWidget(self.portrait_label, 0, Qt.AlignCenter)

                 # === browse for portrait button ===

        self.browse_portrait_button = QPushButton("Browse image...", frame)
        self.browse_portrait_button.clicked.connect(self.browse_for_portrait)
        frame_grid.addWidget(self.browse_portrait_button, 1, Qt.AlignCenter)


    def update_portrait(self, path: str):
        self.pix_path = path
        if self.pix_path == "":
            self.pix_path = self.image_cache['images']['character_portraits']['fluff_placeholder']

        pix = QPixmap(self.pix_path)
        pix = pix.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.portrait_label.setPixmap(pix)

    def on_character_change(self):
        selected_character_name = self.character_select_combobox.currentText()
        if selected_character_name == 'New Character':
            # Clear all fields for new character creation
            self.character_fullname_lineedit.clear()
            self.character_id_lineedit.clear()
            self.character_age_lineedit.clear()
            self.character_species_lineedit.clear()
            self.character_subspecies_lineedit.clear()
            self.character_species_icon_combobox.setCurrentText("none")
            self.character_c_positive_textedit.clear()
            self.character_c_negative_textedit.clear()
            self.character_g_positive_textedit.clear()
            self.character_g_negative_textedit.clear()
            self.character_tags_textedit.clear()
            self.quick_weight_textedit.clear()
            self.character_gender_combobox.setCurrentText("none specified")
            self.update_portrait("")
            self.character_id_lineedit.setReadOnly(False)
            self.copy_character_button.setEnabled(False)
            self.delete_character_button.setEnabled(False)
            self.add_character_button.setEnabled(True)
        else:
            # Load existing character data
            character_data = next((char for char in self.characters if char["nameID"] == selected_character_name), None)
            self.copy_character_button.setEnabled(True)
            self.delete_character_button.setEnabled(True)
            self.add_character_button.setEnabled(False)

            if character_data:
                self.character_id_lineedit.clear()
                self.character_id_lineedit.setText(character_data.get("nameID", ""))
                self.character_age_lineedit.clear()
                self.character_age_lineedit.setText(character_data.get("age", ""))
                self.character_species_lineedit.clear()
                self.character_species_lineedit.setText(character_data.get("species", "")) 
                self.character_subspecies_lineedit.clear()
                self.character_subspecies_lineedit.setText(character_data.get("subspecies", ""))
                species_icon = character_data.get("species icon", "none")
                self.character_species_icon_combobox.setCurrentText(species_icon.capitalize())
                self.character_fullname_lineedit.clear()
                self.character_fullname_lineedit.setText(character_data.get("full_name", ""))

                c_positive = character_data.get("c_positive", "")
                c_positive_list = []
                if c_positive not in ("", None):
                    for tag in c_positive:
                        if tag['strength'] != 1.0:
                            c_positive_list.append(f'{tag['strength']}::{tag['tag']}::')
                        else:
                            c_positive_list.append(tag['tag'])
                    self.character_c_positive_textedit.setPlainText(', '.join(c_positive_list))

                c_negative = character_data.get("c_negative", "")
                c_negative_list = []
                if c_negative not in ("", None):
                    for tag in c_negative:
                        if tag['strength'] != 1.0:
                            c_negative_list.append(f'{tag['strength']}::{tag['tag']}::')
                        else:
                            c_negative_list.append(tag['tag'])
                    self.character_c_negative_textedit.setPlainText(', '.join(c_negative_list))

                g_positive = character_data.get("g_positive", "")
                if g_positive not in ("", None):
                    g_positive_list = []
                    for tag in g_positive:
                        if tag['strength'] != 1.0:
                            g_positive_list.append(f'{tag['strength']}::{tag['tag']}::')
                        else:
                            g_positive_list.append(tag['tag'])
                    self.character_g_positive_textedit.setPlainText(', '.join(g_positive_list))

                g_negative = character_data.get("g_negative", "")
                if g_negative not in ("", None):
                    g_negative_list = []
                    for tag in g_negative:
                        if tag['strength'] != 1.0:
                            g_negative_list.append(f'{tag['strength']}::{tag['tag']}::')
                        else:
                            g_negative_list.append(tag['tag'])
                    self.character_g_negative_textedit.setPlainText(', '.join(g_negative_list))

                self.character_gender_combobox.setCurrentText(character_data.get("gender", "none specified"))

                tags = character_data.get("tags", "") 
                if tags not in ("", None):
                    self.character_tags_textedit.setPlainText(', '.join(tags))

                quick_weights = character_data.get("quick_weights", "")
                quick_weights_list = []
                for qw in quick_weights:
                    quick_weights_list.append(qw['tag'])
                
                self.quick_weight_textedit.setPlainText(', '.join(quick_weights_list))

                self.character_id_lineedit.setReadOnly(True)

                # Update portrait if path exists
                try:
                    portrait_path = self.image_cache['portraits'][selected_character_name.lower()]
                    self.update_portrait(portrait_path)
                except KeyError:
                    self.update_portrait("")


    def browse_for_portrait(self):
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select portrait image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)"
        )

        if not file_path:  # user hit Cancel
            return

        # Always update the preview
        self.update_portrait(file_path)

        selected_character_name = self.character_select_combobox.currentText()

        # For "New Character", just keep pix_path; add_new_character will handle the copy
        if selected_character_name == "New Character":
            return

        # Existing character: save/overwrite their portrait
        self.save_current_portrait_for_character(selected_character_name)



    def save_fullname(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["full_name"] = self.character_fullname_lineedit.text()
                break
    def save_age(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["age"] = self.character_age_lineedit.text()
                break
    def save_species(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["species"] = self.character_species_lineedit.text()
                break
    def save_subspecies(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["subspecies"] = self.character_subspecies_lineedit.text()
                break

    def save_species_icon(self):        
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["species icon"] = self.character_species_icon_combobox.currentText()
                break

    def save_tags(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["tags"] = [tag.strip() for tag in self.character_tags_textedit.toPlainText().split(',') if tag.strip() != '']
                break

    def save_quick_weights(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                new_quick_weights = []
                quick_weights = self.quick_weight_textedit.toPlainText().split(',')
                for tag in quick_weights:
                    if tag.strip() != '':
                        new_quick_weights.append(tag.strip())
                new_quick_weights_dict = []
                for tag in new_quick_weights:
                    new_quick_weights_dict.append({
                    "max": 3,
                    "min": -3,
                    "negative": False,
                    "tag": tag,
                    "value": 0
                    })
                character["quick_weights"] = new_quick_weights_dict
                break

    def save_prompt_field(self, field_name, text_edit):
        current_name = self.character_select_combobox.currentText()
        if current_name == 'New Character':
            return
        else:
            new_prompt = []
            prompt = text_edit.toPlainText().split(',')
            for tag in prompt:
                if '::' in tag:
                    parts = tag.split('::')
                    for part in parts:
                        part = part.strip()
                    strength = float(parts[0])
                    for tag_part in parts[1:]:
                        if tag_part != '':
                            new_prompt.append({"tag": tag_part, "strength": strength})
                        
                else:
                    new_prompt.append({"tag": tag.strip(), "strength": 1})

            for character in self.characters:
                if character["nameID"] == current_name:
                    character[field_name] = new_prompt
                break

    def save_gender(self):
        current_name = self.character_select_combobox.currentText()
        for character in self.characters:
            if character["nameID"] == current_name:
                character["gender"] = self.character_gender_combobox.currentText()
                break
    
    def regenerate_character_list(self):
        self.character_select_combobox.clear()
        self.character_list = [f'{character["nameID"]}' for character in self.characters]
        self.character_list.insert(0, 'New Character')
        self.character_select_combobox.addItems(self.character_list)
    
    def add_new_character(self):
        new_character = {
        "nameID": self.character_id_lineedit.text(),
        "full_name": self.character_fullname_lineedit.text(),
        "c_positive": self.character_c_positive_textedit.toPlainText(),
        "c_negative": self.character_c_negative_textedit.toPlainText(),
        "g_positive": self.character_g_positive_textedit.toPlainText(),
        "g_negative": self.character_g_negative_textedit.toPlainText(),
        "exclusive_chance_tag":"",
        "non_exclusive_chance_tag": "",
        "age": self.character_age_lineedit.text(),
        "gender": self.character_gender_combobox.currentText(), 
        "species": self.character_species_lineedit.text(),
        "subspecies": self.character_subspecies_lineedit.text(),
        "species icon": self.character_species_icon_combobox.currentText(),
        "tags": [],
        "quick_weights": [],
        "quotes": [],
        "outfits": [],
        "most_recent_outfit": "None",
        "tag_associations": []
  }
        
        if not new_character["nameID"]:
            Error(self, "Error: Character ID cannot be empty.")
            return
        
        if any(char["nameID"] == new_character["nameID"] for char in self.characters):
            Error(self, "Error: Character ID must be unique.")
            return
        
        folder_path = Path(REFERENCE_DIR / new_character["nameID"].lower())
        folder_path.mkdir(parents=True, exist_ok=True)

        self.characters.append(new_character)
        self.save_current_portrait_for_character(new_character["nameID"])
        self.regenerate_character_list()
        self.character_select_combobox.setCurrentText(new_character["nameID"])
        print(self.characters)

    def copy_character(self):
        character_to_copy = self.character_select_combobox.currentText()
        self.character_select_combobox.setCurrentIndex(0)  # Switch to 'New Character' to allow adding
        for character in self.characters:
            if character["nameID"] == character_to_copy:
                self.character_id_lineedit.setText(character["nameID"] + "_copy")
                self.character_fullname_lineedit.setText(character["full_name"])
                self.character_age_lineedit.setText(character["age"])
                self.character_species_lineedit.setText(character["species"])
                self.character_subspecies_lineedit.setText(character["subspecies"])
                self.character_species_icon_combobox.setCurrentText(character["species icon"])  
                self.character_c_positive_textedit.setPlainText(character["c_positive"])
                self.character_c_negative_textedit.setPlainText(character["c_negative"])
                self.character_g_positive_textedit.setPlainText(character["g_positive"])
                self.character_g_negative_textedit.setPlainText(character["g_negative"])
                break
    
    def delete_character(self):
        character_to_delete = self.character_select_combobox.currentText()

        dlg = Confirm(self, "Delete character", "Are you sure you want to delete?", "Delete", "Cancel")
        result = dlg.exec()

        if result == QDialog.Accepted:
            # delete their portrait (if any)
            self.delete_portrait_for_character(character_to_delete)

            # delete their reference folder
            character_reference_path = Path(REFERENCE_DIR) / character_to_delete.lower()
            if character_reference_path.exists() and character_reference_path.is_dir():
                try:
                    shutil.rmtree(character_reference_path)
                except OSError:
                    pass

            # delete their character json file
            character_json_path = CHARACTERS_DIR / f"{character_to_delete}.json"
            if character_json_path.is_file():
                try:
                    character_json_path.unlink()
                except OSError:
                    pass  # if delete fails for some reason, just ignore it

            # remove from characters list
            self.characters[:] = [char for char in self.characters if char["nameID"] != character_to_delete]
            self.regenerate_character_list()
            self.character_select_combobox.setCurrentIndex(0)
            

    def closeEvent(self, event):
        # Ensure target folder exists
        characters_dir_path = CHARACTERS_DIR
        characters_dir_path.mkdir(parents=True, exist_ok=True)

        # Write one file per character: data/config/characters/<nameID>.json
        for character in self.characters:
            name_id = str(character.get("nameID", "")).strip()
            if not name_id:
                continue  # skip broken entries

            character_file_path = characters_dir_path / f"{name_id}.json"
            with character_file_path.open("w", encoding="utf-8") as f:
                json.dump(character, f, indent=2, ensure_ascii=False)
        
        refresh_character_lists_signal.reload_character_data.emit()
        refresh_character_lists_signal.refresh_lists.emit()
        event.accept()

    def save_current_portrait_for_character(self, character_id: str):
        """Copy the currently shown portrait into the portraits dir for this character, overwriting any existing one."""

        # No portrait set or using placeholder: nothing to copy
        if not hasattr(self, "pix_path"):
            return
        if not self.pix_path:
            return

        placeholder_path = self.image_cache['images']["portraits"]['fluff_placeholder']
        if self.pix_path == placeholder_path:
            # using the default placeholder, don't copy
            return

        source_path = Path(self.pix_path)
        if not source_path.is_file():
            return

        # normalize to lower case
        character_key = character_id.lower()
        extension = source_path.suffix.lower() or ".png"
        target_path = self.portraits_dir / f"{character_key}{extension}"

        # overwrite any existing portrait for this character
        if target_path.exists():
            try:
                target_path.unlink()
            except OSError:
                return  # bail if we somehow can't delete it

        copy2(source_path, target_path)

        # update cache mapping
        if "character_portraits" in self.image_cache:
            self.image_cache["portraits"][character_key] = str(target_path)


    def delete_portrait_for_character(self, character_id: str):
        """Delete any portrait files for this character (any extension) and clear cache entry."""
        portraits_cache = self.image_cache.setdefault("portraits", {})
        key = character_id.lower()

        # don't delete the shared placeholder image (it lives under image_cache["images"]["character_portraits"])
        placeholder_path = self.image_cache.get("images", {}).get("character_portraits", {}).get("fluff_placeholder", "")

        # delete any file matching <key>.<ext> in portraits dir
        try:
            for portrait_file in Path(self.portraits_dir).glob(f"{key}.*"):
                if portrait_file.is_file():
                    # extra safety: never delete the placeholder even if it matches somehow
                    if placeholder_path and str(portrait_file) == str(Path(placeholder_path)):
                        continue
                    try:
                        portrait_file.unlink()
                    except OSError:
                        pass
        except OSError:
            pass

        # clear cache entry
        portraits_cache.pop(key, None)


        

