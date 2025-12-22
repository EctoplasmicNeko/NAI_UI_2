from PySide6.QtCore import QObject, Signal

class CharacterChangedSignal(QObject):
    character_changed_signal = Signal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # whenever this signal is emitted, also call our debug printer
        self.character_changed_signal.connect(self._debug_print)

    def _debug_print(self, slot_id: int, character_name: str):
        print(f"[CharacterChangedSignal] slot={slot_id}, character={character_name}")

character_changed_signal = CharacterChangedSignal()
