
from PySide6.QtWidgets import QGridLayout, QFrame
from widget import decorated_combobox
from signaling.outfit_changed import outfit_changed_signal


class CharacterPresetTab(QFrame):
    
    def __init__(self, parent, ID):
        super().__init__(parent)
        self.ID = ID
        self.build_character_preset_tab()
        

    def build_character_preset_tab(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 0)
        self.grid.setRowStretch(3, 1)
        self.grid.setRowStretch(4, 0)
        self.grid.setRowStretch(5, 1)
        self.grid.setRowStretch(6, 0)
        self.grid.setRowStretch(7, 1)

        self.outfit_combo = decorated_combobox.DecoratedComboBox(self)
        self.grid.addWidget(self.outfit_combo, 0, 0, 1, 1) 
        self.outfit_combo.currentTextChanged.connect(self.on_outfit_changed)

    def on_outfit_changed(self, new_outfit_name):
        outfit_changed_signal.outfit_changed.emit(new_outfit_name, self.ID)



        

