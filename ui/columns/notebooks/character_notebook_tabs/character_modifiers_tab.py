from PySide6.QtWidgets import QGridLayout, QFrame,QCheckBox, QSpinBox, QLabel
from data.datahub import get_all_characters
from widget.decorated_combobox import DecoratedComboBox


class CharacterModifiersTab(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_character_modifiers_tab()

    def build_character_modifiers_tab(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 0)   
        self.grid.setRowStretch(3, 0)
        self.grid.setRowStretch(4, 1)

        self.auto_change_characters_label = QLabel("Auto-Change Characters Settings", self)
        self.grid.addWidget(self.auto_change_characters_label, 0, 0, 1, 2)
        self.auto_advance_characters_checkbox = QCheckBox("Auto-Advance Characters", self)
        self.auto_advance_characters_checkbox.setToolTip("Automatically advance to the next character after each generation.")
        self.grid.addWidget(self.auto_advance_characters_checkbox, 1, 0) 
        self.auto_advance_characters_checkbox.stateChanged.connect(lambda: self.exclusive_checkboxes(self.auto_advance_characters_checkbox)) 

        self.auto_random_characters_checkbox = QCheckBox("Auto-Random Characters", self)
        self.grid.addWidget(self.auto_random_characters_checkbox, 1, 1)
        self.auto_random_characters_checkbox.setToolTip("Automatically select a random character after each generation.")
        self.auto_random_characters_checkbox.stateChanged.connect(lambda: self.exclusive_checkboxes(self.auto_random_characters_checkbox))

        self.auto_advance_character_frequency_spinbox = QSpinBox(self)
        self.auto_advance_character_frequency_spinbox.setToolTip("Set how many generations to wait before auto-advancing to the next character.")
        self.auto_advance_character_frequency_spinbox.setMinimum(0)  
        self.auto_advance_character_frequency_spinbox.setValue(1)  
        self.auto_advance_character_frequency_spinbox.setSpecialValueText("Frequency: On Set")
        self.grid.addWidget(self.auto_advance_character_frequency_spinbox, 2, 0, 1, 2)
        self.auto_advance_character_frequency_spinbox.setPrefix("Frequency: ")

        self.auto_advance_character_tag1_combo = DecoratedComboBox(self)
        self.auto_advance_character_tag1_combo.addItems(["None"] + list(self.load_tags()))
        self.auto_advance_character_tag1_combo.setPrefix("Filter: ")
        self.grid.addWidget(self.auto_advance_character_tag1_combo, 3, 0)
        self.auto_advance_character_tag1_combo.setToolTip( "Select the tag that determines character pool for auto-advancing.")

        self.auto_advance_character_tag2_combo = DecoratedComboBox(self)
        self.auto_advance_character_tag2_combo.addItems(["None"] + list(self.load_tags()))
        self.grid.addWidget(self.auto_advance_character_tag2_combo, 3, 1)
        self.auto_advance_character_tag2_combo.setPrefix("Filter: ")
        self.auto_advance_character_tag2_combo.setToolTip( "Select the tag that determines character pool for auto-advancing.")
        

    def load_tags(self):
        self.characters = get_all_characters()
        tag_list = []
        for character in self.characters:
            for tag in character.get("tags", []):
                if tag not in tag_list:
                    tag_list.append(tag)
            
        return tag_list
    
    def reload_tags(self):
        current_tag1 = self.auto_advance_character_tag1_combo.currentText()
        current_tag2 = self.auto_advance_character_tag2_combo.currentText()
        self.auto_advance_character_tag1_combo.clear()
        self.auto_advance_character_tag2_combo.clear()
        self.characters = get_all_characters()
        tag_list = []
        for character in self.characters:
            for tag in character.get("tags", []):
                if tag not in tag_list:
                    tag_list.append(tag)
            
        self.auto_advance_character_tag1_combo.addItems(["None"] + tag_list)
        self.auto_advance_character_tag2_combo.addItems(["None"] + tag_list)
        if current_tag1 in tag_list:
            self.auto_advance_character_tag1_combo.setCurrentText(current_tag1)
        else:
            self.auto_advance_character_tag1_combo.setCurrentText("None")

        if current_tag2 in tag_list:
            self.auto_advance_character_tag2_combo.setCurrentText(current_tag2)
        else:
            self.auto_advance_character_tag2_combo.setCurrentText("None")
    
    def exclusive_checkboxes(self, checked_checkbox):
        if checked_checkbox == self.auto_advance_characters_checkbox and checked_checkbox.isChecked():
            self.auto_random_characters_checkbox.setChecked(False)
        elif checked_checkbox == self.auto_random_characters_checkbox and checked_checkbox.isChecked():
            self.auto_advance_characters_checkbox.setChecked(False)