from PySide6.QtCore import QObject, Signal

class MinimalCharacterTab(QObject):
    on_signal = Signal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)

minimal_character_tab = MinimalCharacterTab()