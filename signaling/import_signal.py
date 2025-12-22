# signaling/import_signal.py
from PySide6.QtCore import QObject, Signal

class ImportSignalBus(QObject):
    # path, dict_type, metadata, prompt, characters, settings, seed
    import_signal = Signal(str, dict, bool, bool, bool, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.import_signal.connect(self.debug_print)

    def debug_print(self, dict_type: str, metadata: dict,
                    import_prompt: bool, import_characters: bool,
                    import_settings: bool, import_seed: bool):
        print(
            f"dict_type={dict_type}, "
            f"import_prompt={import_prompt}, import_characters={import_characters}, "
            f"import_settings={import_settings}, import_seed={import_seed}"
        )

# single shared bus
import_signal = ImportSignalBus()
