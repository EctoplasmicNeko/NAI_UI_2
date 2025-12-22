# windows/import_on_drop.py
from PySide6.QtWidgets import QDialog, QGridLayout, QCheckBox, QPushButton
from signaling.import_signal import import_signal

class ImportDialog(QDialog):
    def __init__(self, parent, path, dict_type, metadata, import_settings_state, import_prompt_state, import_seed_state, import_characters_state):
        super().__init__(parent)
        self.path = path
        self.dict_type = dict_type
        self.metadata = metadata
        self.import_settings_state = import_settings_state
        self.import_prompt_state = import_prompt_state
        self.import_seed_state = import_seed_state
        self.import_characters_state = import_characters_state

        self.setWindowTitle("Import")
        self.build_import_window()

    def build_import_window(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.prompt_checkbox = QCheckBox("Import Prompt", self)
        self.prompt_checkbox.setChecked(self.import_prompt_state)
        self.grid.addWidget(self.prompt_checkbox, 0, 0)

        self.import_characters_checkbox = QCheckBox("Import Characters", self)
        self.import_characters_checkbox.setChecked(self.import_characters_state)
        self.grid.addWidget(self.import_characters_checkbox, 1, 0)

        self.import_settings_checkbox = QCheckBox("Import Settings", self)
        self.import_settings_checkbox.setChecked(self.import_settings_state)
        self.grid.addWidget(self.import_settings_checkbox, 2, 0)

        self.import_seed_checkbox = QCheckBox("Import Seed", self)
        self.import_seed_checkbox.setChecked(self.import_seed_state)
        self.grid.addWidget(self.import_seed_checkbox, 3, 0)

        self.import_button = QPushButton("Import", self)
        self.import_button.clicked.connect(self.on_import_clicked)
        self.grid.addWidget(self.import_button, 4, 0)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        self.grid.addWidget(self.cancel_button, 5, 0)

    def on_import_clicked(self):
        import_signal.import_signal.emit(
            self.dict_type,
            self.metadata,
            self.import_settings_checkbox.isChecked(),
            self.prompt_checkbox.isChecked(),
            self.import_seed_checkbox.isChecked(),
            self.import_characters_checkbox.isChecked(),
        )
        self.close()
