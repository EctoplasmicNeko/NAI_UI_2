from PySide6.QtCore import QObject, Signal

class CharacterChangedSignal(QObject):
    character_changed_signal = Signal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

character_changed_signal = CharacterChangedSignal()
