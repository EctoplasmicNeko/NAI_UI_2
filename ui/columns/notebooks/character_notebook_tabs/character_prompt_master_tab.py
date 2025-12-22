from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox, QTextEdit, QCheckBox, QSpinBox, QLabel, QPushButton, QSizePolicy, QSpacerItem
from ui.columns.notebooks.character_notebook_tabs.character_quick_tab import CharacterQuickTab
from ui.columns.notebooks.character_notebook_tabs.character_prompt_tab import CharacterPromptTab

class CharacterPromptMasterTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_character_prompt_master_tab()

    def build_character_prompt_master_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 0)

        self.prompt_tab = CharacterPromptTab(self)
        self.grid.addWidget(self.prompt_tab, 0, 0)

        self.quick_weights_tab = CharacterQuickTab(self)
        self.grid.addWidget(self.quick_weights_tab, 1, 0)
        
