from PySide6.QtCore import QObject, Signal

class CharacterSortSignal(QObject):
    request_character_sort_type = Signal()
    return_character_sort_type = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

character_sort_signal = CharacterSortSignal()