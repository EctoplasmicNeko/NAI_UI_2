from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QDialog, QGridLayout, QComboBox, QLineEdit, QTextEdit, QFrame, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSignalBlocker

from windows.error import Error
from windows.confirmation import Confirm
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
        self.characters_file_path = CHARACTERS_DIR
        self.portraits_dir = PORTRAITS_DIR

        self.build_manage_character_window()
        self.on_character_change()

    def build_manage_character_window(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.characters = get_all_characters()
        self.character_list = [f'{character["nameID"]}' for character in self.characters]
        self.character_list.insert(0, "New Character")

        self.button_frame = QFrame(self)
        self.grid.addWidget(self.button_frame, 0, 0, 1, 3)

        self.button_frame_grid = QGridLayout(self.button_frame)

        self.add_character_button = QPushButton("Add Character", self)
        self.add_character_button.clicked.connect(self.add_new_character)
        self.button_frame_grid.addWidget(self.add_character_button, 0, 0)

        self.delete_character_button = QPushButton("Delete Character", self)
        self.delete_character_button.clicked.connect(self.delete_character)
        self.button_frame_grid.addWidget(self.delete_character_button, 0, 1)

        self.copy_character_button = QPushButton("Copy Character", self)
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
        self.character_fullname_label.setText("Full Name")
        self.grid.addWidget(self.character_fullname_label, 3, 0)

        self.character_fullname_lineedit = QLineEdit(self)
        self.character_fullname_lineedit.setPlaceholderText("Full Name")
        self.character_fullname_lineedit.setToolTip("The character's full name (longer, more descriptive)")
        self.character_fullname_lineedit.editingFinished.connect(self.save_fullname)
        self.grid.addWidget(self.character_fullname_lineedit, 3, 1)

        self.character_age_label = QLabel("Age:", self)
        self.character_age_label.setText("Age")
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
        self.character_gender_combobox.addItems(["none specified", "Male", "Female", "Other"])
        self.character_gender_combobox.setEditable(False)
        self.character_gender_combobox.setCurrentText("none specified")
        self.character_gender_combobox.currentIndexChanged.connect(self.save_gender)
        self.grid.addWidget(self.character_gender_combobox, 5, 1)

        self.character_species_label = QLabel("Species:", self)
        self.character_species_label.setText("Species")
        self.grid.addWidget(self.character_species_label, 6, 0)

        self.character_species_lineedit = QLineEdit(self)
        self.character_species_lineedit.setPlaceholderText("Species")
        self.character_species_lineedit.setToolTip("The character's species")
        self.character_species_lineedit.editingFinished.connect(self.save_species)
        self.grid.addWidget(self.character_species_lineedit, 6, 1)

        self.character_subspecies_label = QLabel("Subspecies:", self)
        self.character_subspecies_label.setText("Subspecies")
        self.grid.addWidget(self.character_subspecies_label, 7, 0)

        self.character_subspecies_lineedit = QLineEdit(self)
        self.character_subspecies_lineedit.setPlaceholderText("Subspecies")
        self.character_subspecies_lineedit.setToolTip("The character's subspecies")
        self.character_subspecies_lineedit.editingFinished.connect(self.save_subspecies)
        self.grid.addWidget(self.character_subspecies_lineedit, 7, 1)

        self.character_species_icon_label = QLabel("Species Icon:", self)
        self.character_species_icon_label.setText("Species Icon")
        self.grid.addWidget(self.character_species_icon_label, 8, 0)

        self.character_species_icon_combobox = QComboBox(self)
        self.character_species_icon_combobox.setToolTip("Icon representing the character's species")
        self.character_species_icon_combobox.addItems(["None", "Human", "Cat", "Dog", "Fox", "Rabbit", "Squirrel", "Angel", "Demon"])
        self.character_species_icon_combobox.setEditable(False)
        self.character_species_icon_combobox.setCurrentText("None")
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

        self.character_g_positive_textedit = QTextEdit(self)
        self.character_g_positive_textedit.setPlaceholderText("Add to Positive Global Prompt")
        self.character_g_positive_textedit.textChanged.connect(lambda: self.save_prompt_field("g_positive", self.character_g_positive_textedit))
        self.grid.addWidget(self.character_g_positive_textedit, 14, 0, 1, 3)

        self.character_g_negative_label = QLabel("Global Negative Prompt Additions", self)
        self.character_g_negative_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_g_negative_label, 15, 0, 1, 3)

        self.character_g_negative_textedit = QTextEdit(self)
        self.character_g_negative_textedit.setPlaceholderText("Add to Negative Global Prompt:")
        self.character_g_negative_textedit.textChanged.connect(lambda: self.save_prompt_field("g_negative", self.character_g_negative_textedit))
        self.grid.addWidget(self.character_g_negative_textedit, 16, 0, 1, 3)

        self.character_tags_label = QLabel("Tags", self)
        self.character_tags_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.character_tags_label, 17, 0, 1, 3)

        self.character_tags_textedit = QTextEdit(self)
        self.character_tags_textedit.setPlaceholderText("Add to Tags:")
        self.character_tags_textedit.textChanged.connect(self.save_tags)
        self.grid.addWidget(self.character_tags_textedit, 18, 0, 1, 3)

        self.quick_weight_label = QLabel("Quick Weights", self)
        self.quick_weight_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.quick_weight_label, 19, 0, 1, 3)

        self.quick_weight_textedit = QTextEdit(self)
        self.quick_weight_textedit.setPlaceholderText("Add to Quick Weights:")
        self.quick_weight_textedit.textChanged.connect(self.save_quick_weights)
        self.grid.addWidget(self.quick_weight_textedit, 20, 0, 1, 3)

        frame = QFrame(self)
        frame.setMinimumSize(170, 170)

        frame_grid = QVBoxLayout(frame)
        frame_grid.setContentsMargins(6, 6, 6, 6)
        frame_grid.setSpacing(4)

        self.grid.addWidget(frame, 2, 2, 6, 1)

        self.portrait_label = QLabel(frame)
        self.portrait_label.setAlignment(Qt.AlignCenter)
        self.portrait_label.setFixedSize(150, 150)
        frame_grid.addWidget(self.portrait_label, 0, Qt.AlignCenter)

        self.browse_portrait_button = QPushButton("Browse image...", frame)
        self.browse_portrait_button.clicked.connect(self.browse_for_portrait)
        frame_grid.addWidget(self.browse_portrait_button, 1, Qt.AlignCenter)

    def update_portrait(self, path: str):
        self.pix_path = path

        if not self.pix_path:
            self.pix_path = self.image_cache["images"]["character_portraits"]["fluff_placeholder"]

        pixmap = QPixmap(self.pix_path)
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        self.portrait_label.setPixmap(scaled_pixmap)

    def browse_for_portrait(self):
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select portrait image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All Files (*)"
        )

        if not file_path:
            return

        self.update_portrait(file_path)

        selected_character_name = self.character_select_combobox.currentText()
        if selected_character_name == "New Character":
            return

        self.save_current_portrait_for_character(selected_character_name)

    def on_character_change(self):
        selected_character_name = self.character_select_combobox.currentText()

        if selected_character_name == "New Character":
            self.set_lineedit_text_safely(self.character_fullname_lineedit, "")
            self.set_lineedit_text_safely(self.character_id_lineedit, "")
            self.set_lineedit_text_safely(self.character_age_lineedit, "")
            self.set_lineedit_text_safely(self.character_species_lineedit, "")
            self.set_lineedit_text_safely(self.character_subspecies_lineedit, "")

            combobox_blocker_species_icon = QSignalBlocker(self.character_species_icon_combobox)
            self.character_species_icon_combobox.setCurrentText("None")
            del combobox_blocker_species_icon

            combobox_blocker_gender = QSignalBlocker(self.character_gender_combobox)
            self.character_gender_combobox.setCurrentText("none specified")
            del combobox_blocker_gender

            self.set_textedit_text_safely(self.character_c_positive_textedit, "")
            self.set_textedit_text_safely(self.character_c_negative_textedit, "")
            self.set_textedit_text_safely(self.character_g_positive_textedit, "")
            self.set_textedit_text_safely(self.character_g_negative_textedit, "")
            self.set_textedit_text_safely(self.character_tags_textedit, "")
            self.set_textedit_text_safely(self.quick_weight_textedit, "")

            self.update_portrait("")

            self.character_id_lineedit.setReadOnly(False)
            self.copy_character_button.setEnabled(False)
            self.delete_character_button.setEnabled(False)
            self.add_character_button.setEnabled(True)
            return

        character_data = next((char for char in self.characters if char["nameID"] == selected_character_name), None)

        self.copy_character_button.setEnabled(True)
        self.delete_character_button.setEnabled(True)
        self.add_character_button.setEnabled(False)

        if not character_data:
            return

        self.set_lineedit_text_safely(self.character_id_lineedit, str(character_data.get("nameID", "")))
        self.set_lineedit_text_safely(self.character_age_lineedit, str(character_data.get("age", "")))
        self.set_lineedit_text_safely(self.character_species_lineedit, str(character_data.get("species", "")))
        self.set_lineedit_text_safely(self.character_subspecies_lineedit, str(character_data.get("subspecies", "")))
        self.set_lineedit_text_safely(self.character_fullname_lineedit, str(character_data.get("full_name", "")))

        combobox_blocker_gender = QSignalBlocker(self.character_gender_combobox)
        self.character_gender_combobox.setCurrentText(str(character_data.get("gender", "none specified")))
        del combobox_blocker_gender

        combobox_blocker_species_icon = QSignalBlocker(self.character_species_icon_combobox)
        self.character_species_icon_combobox.setCurrentText(str(character_data.get("species icon", "None")))
        del combobox_blocker_species_icon

        c_positive_text = self.format_prompt_list(character_data.get("c_positive", []))
        c_negative_text = self.format_prompt_list(character_data.get("c_negative", []))
        g_positive_text = self.format_prompt_list(character_data.get("g_positive", []))
        g_negative_text = self.format_prompt_list(character_data.get("g_negative", []))

        self.set_textedit_text_safely(self.character_c_positive_textedit, c_positive_text)
        self.set_textedit_text_safely(self.character_c_negative_textedit, c_negative_text)
        self.set_textedit_text_safely(self.character_g_positive_textedit, g_positive_text)
        self.set_textedit_text_safely(self.character_g_negative_textedit, g_negative_text)

        tags_value = character_data.get("tags", []) or []
        tags_text = ", ".join([str(tag).strip() for tag in tags_value if str(tag).strip()])
        self.set_textedit_text_safely(self.character_tags_textedit, tags_text)

        quick_weights_value = character_data.get("quick_weights", []) or []
        quick_weight_tags = []
        for quick_weight_item in quick_weights_value:
            tag_value = str(quick_weight_item.get("tag", "")).strip()
            if tag_value:
                quick_weight_tags.append(tag_value)

        quick_weights_text = ", ".join(quick_weight_tags)
        self.set_textedit_text_safely(self.quick_weight_textedit, quick_weights_text)

        self.character_id_lineedit.setReadOnly(True)

        try:
            portrait_path = self.image_cache["portraits"][selected_character_name.lower()]
            self.update_portrait(portrait_path)
        except Exception:
            self.update_portrait("")

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

    def save_gender(self):
        current_name = self.character_select_combobox.currentText()

        for character in self.characters:
            if character["nameID"] == current_name:
                character["gender"] = self.character_gender_combobox.currentText()
                break

    def save_tags(self):
        current_name = self.character_select_combobox.currentText()
        if current_name == "New Character":
            return

        raw_tags_text = self.character_tags_textedit.toPlainText()
        raw_tag_chunks = raw_tags_text.split(",")

        cleaned_tags = []
        for raw_chunk in raw_tag_chunks:
            cleaned_chunk = raw_chunk.strip()
            if cleaned_chunk:
                cleaned_tags.append(cleaned_chunk)

        for character in self.characters:
            if character["nameID"] == current_name:
                character["tags"] = cleaned_tags
                break

    def save_quick_weights(self):
        current_name = self.character_select_combobox.currentText()
        if current_name == "New Character":
            return

        raw_quick_weights_text = self.quick_weight_textedit.toPlainText()
        raw_quick_weight_chunks = raw_quick_weights_text.split(",")

        cleaned_quick_weight_tags = []
        for raw_chunk in raw_quick_weight_chunks:
            cleaned_chunk = raw_chunk.strip()
            if cleaned_chunk:
                cleaned_quick_weight_tags.append(cleaned_chunk)

        quick_weight_dicts = []
        for tag in cleaned_quick_weight_tags:
            quick_weight_dicts.append(
                {
                    "max": 3,
                    "min": -3,
                    "negative": False,
                    "tag": tag,
                    "value": 0
                }
            )

        for character in self.characters:
            if character["nameID"] == current_name:
                character["quick_weights"] = quick_weight_dicts
                break

    def save_prompt_field(self, field_name, text_edit):
        current_name = self.character_select_combobox.currentText()
        if current_name == "New Character":
            return

        raw_prompt_text = text_edit.toPlainText()
        parsed_prompt = self.parse_prompt_text(raw_prompt_text)

        for character in self.characters:
            if character["nameID"] == current_name:
                character[field_name] = parsed_prompt
                break

    def regenerate_character_list(self):
        combobox_blocker = QSignalBlocker(self.character_select_combobox)

        self.character_select_combobox.clear()
        self.character_list = [f'{character["nameID"]}' for character in self.characters]
        self.character_list.insert(0, "New Character")
        self.character_select_combobox.addItems(self.character_list)

        del combobox_blocker

    def add_new_character(self):
        initial_c_positive = self.parse_prompt_text(self.character_c_positive_textedit.toPlainText())
        initial_c_negative = self.parse_prompt_text(self.character_c_negative_textedit.toPlainText())
        initial_g_positive = self.parse_prompt_text(self.character_g_positive_textedit.toPlainText())
        initial_g_negative = self.parse_prompt_text(self.character_g_negative_textedit.toPlainText())

        tags_text = self.character_tags_textedit.toPlainText()
        raw_tag_chunks = tags_text.split(",")

        initial_tags = []
        for raw_tag in raw_tag_chunks:
            cleaned_tag = raw_tag.strip()
            if cleaned_tag:
                initial_tags.append(cleaned_tag)

        quick_weights_text = self.quick_weight_textedit.toPlainText()
        raw_quick_weight_chunks = quick_weights_text.split(",")

        cleaned_quick_weight_tags = []
        for raw_chunk in raw_quick_weight_chunks:
            cleaned_chunk = raw_chunk.strip()
            if cleaned_chunk:
                cleaned_quick_weight_tags.append(cleaned_chunk)

        cleaned_initial_quick_weights = []
        for tag in cleaned_quick_weight_tags:
            cleaned_initial_quick_weights.append(
                {
                    "max": 3,
                    "min": -3,
                    "negative": False,
                    "tag": tag,
                    "value": 0
                }
            )

        new_character = {
            "nameID": self.character_id_lineedit.text(),
            "full_name": self.character_fullname_lineedit.text(),
            "c_positive": initial_c_positive,
            "c_negative": initial_c_negative,
            "g_positive": initial_g_positive,
            "g_negative": initial_g_negative,
            "exclusive_chance_tag": "",
            "non_exclusive_chance_tag": "",
            "age": self.character_age_lineedit.text(),
            "gender": self.character_gender_combobox.currentText(),
            "species": self.character_species_lineedit.text(),
            "subspecies": self.character_subspecies_lineedit.text(),
            "species icon": self.character_species_icon_combobox.currentText(),
            "tags": initial_tags,
            "quick_weights": cleaned_initial_quick_weights,
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
        self.on_character_change()

    def copy_character(self):
        character_to_copy = self.character_select_combobox.currentText()
        character_data = next((character for character in self.characters if character["nameID"] == character_to_copy), None)

        if not character_data:
            return

        self.character_select_combobox.setCurrentIndex(0)
        self.on_character_change()

        self.character_id_lineedit.setText(str(character_data.get("nameID", "")) + "_copy")
        self.character_fullname_lineedit.setText(str(character_data.get("full_name", "")))
        self.character_age_lineedit.setText(str(character_data.get("age", "")))
        self.character_species_lineedit.setText(str(character_data.get("species", "")))
        self.character_subspecies_lineedit.setText(str(character_data.get("subspecies", "")))

        self.character_species_icon_combobox.setCurrentText(str(character_data.get("species icon", "None")))
        self.character_gender_combobox.setCurrentText(str(character_data.get("gender", "none specified")))

        self.character_c_positive_textedit.setPlainText(self.format_prompt_list(character_data.get("c_positive", [])))
        self.character_c_negative_textedit.setPlainText(self.format_prompt_list(character_data.get("c_negative", [])))
        self.character_g_positive_textedit.setPlainText(self.format_prompt_list(character_data.get("g_positive", [])))
        self.character_g_negative_textedit.setPlainText(self.format_prompt_list(character_data.get("g_negative", [])))

        tags_value = character_data.get("tags", []) or []
        self.character_tags_textedit.setPlainText(", ".join([str(tag).strip() for tag in tags_value if str(tag).strip()]))

        quick_weights_value = character_data.get("quick_weights", []) or []
        quick_weight_tags = []
        for quick_weight_item in quick_weights_value:
            tag_value = str(quick_weight_item.get("tag", "")).strip()
            if tag_value:
                quick_weight_tags.append(tag_value)

        self.quick_weight_textedit.setPlainText(", ".join(quick_weight_tags))

    def delete_character(self):
        character_to_delete = self.character_select_combobox.currentText()
        if character_to_delete == "New Character":
            return

        dlg = Confirm(self, "Delete character", "Are you sure you want to delete?", "Delete", "Cancel")
        result = dlg.exec()

        if result == QDialog.Accepted:
            self.delete_portrait_for_character(character_to_delete)

            character_reference_path = Path(REFERENCE_DIR) / character_to_delete.lower()
            if character_reference_path.exists() and character_reference_path.is_dir():
                try:
                    shutil.rmtree(character_reference_path)
                except OSError:
                    pass

            character_json_path = CHARACTERS_DIR / f"{character_to_delete}.json"
            if character_json_path.is_file():
                try:
                    character_json_path.unlink()
                except OSError:
                    pass

            self.characters[:] = [char for char in self.characters if char["nameID"] != character_to_delete]

            self.regenerate_character_list()
            self.character_select_combobox.setCurrentIndex(0)
            self.on_character_change()

    def closeEvent(self, event):
        characters_dir_path = CHARACTERS_DIR
        characters_dir_path.mkdir(parents=True, exist_ok=True)

        for character in self.characters:
            name_id = str(character.get("nameID", "")).strip()
            if not name_id:
                continue

            character_file_path = characters_dir_path / f"{name_id}.json"
            try:
                with character_file_path.open("w", encoding="utf-8") as file_handle:
                    json.dump(character, file_handle, indent=2, ensure_ascii=False)
            except OSError:
                pass

        refresh_character_lists_signal.reload_character_data.emit()
        refresh_character_lists_signal.refresh_lists.emit()

        event.accept()

    def save_current_portrait_for_character(self, character_id: str):
        if not hasattr(self, "pix_path"):
            return

        if not self.pix_path:
            return

        placeholder_path = self.image_cache["images"]["character_portraits"]["fluff_placeholder"]
        if self.pix_path == placeholder_path:
            return

        source_path = Path(self.pix_path)
        if not source_path.is_file():
            return

        character_key = character_id.lower()
        extension = source_path.suffix.lower() or ".png"
        target_path = self.portraits_dir / f"{character_key}{extension}"

        try:
            for existing_portrait_file in Path(self.portraits_dir).glob(f"{character_key}.*"):
                if existing_portrait_file.is_file():
                    try:
                        existing_portrait_file.unlink()
                    except OSError:
                        pass
        except OSError:
            pass

        try:
            copy2(source_path, target_path)
        except OSError:
            return

        portraits_cache = self.image_cache.setdefault("portraits", {})
        portraits_cache[character_key] = str(target_path)

    def delete_portrait_for_character(self, character_id: str):
        portraits_cache = self.image_cache.setdefault("portraits", {})
        key = character_id.lower()

        placeholder_path = self.image_cache["images"]["character_portraits"]["fluff_placeholder"]

        try:
            for portrait_file in Path(self.portraits_dir).glob(f"{key}.*"):
                if portrait_file.is_file():
                    if placeholder_path and str(portrait_file) == str(Path(placeholder_path)):
                        continue
                    try:
                        portrait_file.unlink()
                    except OSError:
                        pass
        except OSError:
            pass

        portraits_cache.pop(key, None)

    def set_lineedit_text_safely(self, line_edit: QLineEdit, text: str):
        signal_blocker = QSignalBlocker(line_edit)
        line_edit.setText(text)
        del signal_blocker

    def set_textedit_text_safely(self, text_edit: QTextEdit, text: str):
        signal_blocker = QSignalBlocker(text_edit)
        text_edit.setPlainText(text)
        del signal_blocker

    def parse_prompt_text(self, raw_text: str):
        parsed_prompt = []

        raw_chunks = raw_text.split(",")
        for raw_chunk in raw_chunks:
            chunk = raw_chunk.strip()
            if not chunk:
                continue

            if "::" in chunk:
                parts = [part.strip() for part in chunk.split("::")]
                if not parts:
                    continue

                try:
                    strength_value = float(parts[0])
                except ValueError:
                    continue

                for tag_part in parts[1:]:
                    cleaned_tag_part = tag_part.strip()
                    if cleaned_tag_part:
                        parsed_prompt.append({"tag": cleaned_tag_part, "strength": strength_value})
            else:
                parsed_prompt.append({"tag": chunk, "strength": 1.0})

        return parsed_prompt

    def format_prompt_list(self, prompt_list):
        if not prompt_list:
            return ""

        formatted_chunks = []

        for item in prompt_list:
            tag_text = str(item.get("tag", "")).strip()
            if not tag_text:
                continue

            try:
                strength_value = float(item.get("strength", 1.0))
            except (TypeError, ValueError):
                strength_value = 1.0

            if strength_value != 1.0:
                formatted_chunks.append(f"{strength_value}::{tag_text}::")
            else:
                formatted_chunks.append(tag_text)

        return ", ".join(formatted_chunks)
