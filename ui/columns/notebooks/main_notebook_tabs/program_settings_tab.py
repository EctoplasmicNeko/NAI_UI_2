from PySide6.QtWidgets import QGridLayout, QFrame,  QLabel,QLineEdit, QPushButton
from widget import decorated_combobox
from data.paths import THEMES_DIR
from pathlib import Path
from signaling.speciesbaronoff import species_bar_on_off
from signaling.minimal_character_tab import minimal_character_tab
from windows.confirmation import Confirm
from PySide6.QtWidgets import QDialog



class ProgramSettingsTab(QFrame):

    def __init__(self, parent, image_cache):
        super().__init__(parent,)
        self.image_cache = image_cache
        self.available_themes = self.load_available_themes()
        self.build_program_settings_tab()

    def build_program_settings_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 0)
        self.grid.setRowStretch(3, 0)
        self.grid.setRowStretch(4, 0)
        self.grid.setRowStretch(5, 0)
        self.grid.setRowStretch(6, 1)

        self.password_label = QLabel('NAI API Key')
        self.grid.addWidget(self.password_label, 0, 0)

        self.API_entry = QLineEdit(self)
        self.grid.addWidget(self.API_entry, 0, 1)

        self.manage_characters_button = QPushButton('Manage Characters', self)
        self.grid.addWidget(self.manage_characters_button, 1, 0)
        
        self.manage_presets_button = QPushButton('Manage Presets', self)
        self.grid.addWidget(self.manage_presets_button, 2, 0)       

        self.manage_wildcard_button = QPushButton('Manage Wildcards', self)
        self.grid.addWidget(self.manage_wildcard_button, 3, 0)

        self.manage_assistants_button = QPushButton('Manage Assistants', self)
        self.grid.addWidget(self.manage_assistants_button, 4, 0)

        self.generate_button = QPushButton('Generate')
        self.grid.addWidget(self.generate_button, 5, 0)

        self.test_button = QPushButton('Test')
        self.grid.addWidget(self.test_button, 6, 0)

        self.theme_combo = decorated_combobox.DecoratedComboBox(self)
        self.theme_combo.setPrefix("Theme: ")
        self.theme_combo.addItems(self.available_themes)
        self.grid.addWidget(self.theme_combo, 7, 0) 

        self.enable_species_bar_checkbox = QPushButton('Enable Species Bar', self)
        self.enable_species_bar_checkbox.toggled.connect(self.hide_species_bar)
        self.enable_species_bar_checkbox.setCheckable(True)
        self.grid.addWidget(self.enable_species_bar_checkbox, 1, 1)

        self.enable_character_fluff_tab_checkbox = QPushButton('Enable Character Fluff Tab', self)
        self.enable_character_fluff_tab_checkbox.toggled.connect(self.hide_character_fluff_tab)
        self.enable_character_fluff_tab_checkbox.setCheckable(True)
        self.grid.addWidget(self.enable_character_fluff_tab_checkbox, 2, 1)

        self.enable_reference_image_b64_capture_checkbox = QPushButton('Embed References', self)
        self.enable_reference_image_b64_capture_checkbox.toggled.connect(self.enable_b64_capture)
        self.enable_reference_image_b64_capture_checkbox.setCheckable(True)
        self.grid.addWidget(self.enable_reference_image_b64_capture_checkbox, 3, 1)

        self.character_sorting_combo = decorated_combobox.DecoratedComboBox(self)
        self.character_sorting_combo.setPrefix("Character Sorting: ")
        self.character_sorting_combo.addItems(["Status", "Alphabetical", "Youngest", "Oldest"])
        self.grid.addWidget(self.character_sorting_combo, 4, 1)

        self.write_hydrus_sidecar_checkbox = QPushButton('Write Hydrus Sidecar Files', self)
        self.write_hydrus_sidecar_checkbox.setCheckable(True)
        self.grid.addWidget(self.write_hydrus_sidecar_checkbox, 5, 1)


    def export_state(self):
        return{
            'API_key': self.API_entry.text(),
            'selected_theme': self.theme_combo.currentText(),
            'enable_species_bar': self.enable_species_bar_checkbox.isChecked(),
            'enable_character_fluff_tab': self.enable_character_fluff_tab_checkbox.isChecked(),
            'enable_reference_image_b64_capture': self.enable_reference_image_b64_capture_checkbox.isChecked(),
            'enable_hydrus_sidecar': self.write_hydrus_sidecar_checkbox.isChecked()     
        }

    def import_state(self, loaded):
        self.API_entry.setText(loaded['API_key'])
        self.theme_combo.setCurrentText(loaded['selected_theme'])   
        self.enable_species_bar_checkbox.setChecked(loaded.get('enable_species_bar', False))
        self.hide_species_bar()

        self.enable_character_fluff_tab_checkbox.setChecked(loaded.get('enable_character_fluff_tab', False))
        self.hide_character_fluff_tab()

        self.enable_reference_image_b64_capture_checkbox.blockSignals(True)
        self.enable_reference_image_b64_capture_checkbox.setChecked(loaded.get('enable_reference_image_b64_capture', False))
        self.enable_reference_image_b64_capture_checkbox.blockSignals(False)
        self.enable_b64_capture(loaded.get('enable_reference_image_b64_capture', False), startup=True)
        
        self.write_hydrus_sidecar_checkbox.setChecked(loaded.get('enable_hydrus_sidecar', False))

    def load_available_themes(self):
            themes_dir = Path(THEMES_DIR)
            themes = []

            for file in themes_dir.iterdir():
                if file.is_file() and file.suffix == ".qss":
                    themes.append(file.stem)   # "dark", "fruit_salad", etc.

            return sorted(themes)
    
    def hide_species_bar(self):
        checked = self.enable_species_bar_checkbox.isChecked()
        species_bar_on_off.on_signal.emit(checked)
        if checked:
            self.enable_species_bar_checkbox.setText('Species Bar (On)')
        else:
            self.enable_species_bar_checkbox.setText('Species Bar (Off)')

    def hide_character_fluff_tab(self):
        checked = self.enable_character_fluff_tab_checkbox.isChecked()
        minimal_character_tab.on_signal.emit(checked)
        if checked:
            self.enable_character_fluff_tab_checkbox.setText('Character Fluff Tab (On)')
        else:
            self.enable_character_fluff_tab_checkbox.setText('Character Fluff Tab (Off)')



    def enable_b64_capture(self, checked: bool, startup: bool = False):
        if not startup:
            if checked:
                dialog = Confirm(
                    self,
                    "Enable B64 Capture",
                    "Enabling B64 capture will increase metadata size significantly. "
                    "Are you sure you want to enable this feature?",
                    "Enable",
                    "Cancel"
                )
                if dialog.exec() == QDialog.Accepted:
                    # Already checked at this point
                    self.enable_reference_image_b64_capture_checkbox.setText("Embed References (On)")
                else:
                    # User cancelled – revert checkbox without re-triggering the slot
                    cb = self.enable_reference_image_b64_capture_checkbox
                    cb.blockSignals(True)
                    cb.setChecked(False)
                    cb.blockSignals(False)
                    cb.setText("Embed References (Off)")
            else:
                # Just turned off normally
                self.enable_reference_image_b64_capture_checkbox.setText("Embed References (Off)")
        else:
            # Startup case
            if checked:
                self.enable_reference_image_b64_capture_checkbox.setText("Embed References (On)")
            else:
                self.enable_reference_image_b64_capture_checkbox.setText("Embed References (Off)")
