
from PySide6.QtCore import QObject, Signal

class CycleCharacterSignal(QObject):
    character_cycle_signal = Signal(str, int)

    
    def __init__(self, parent = None):
        super().__init__(parent)

cycle_character_signal = CycleCharacterSignal()