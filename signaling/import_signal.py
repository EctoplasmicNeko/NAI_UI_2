# signaling/import_signal.py
from PySide6.QtCore import QObject, Signal

class ImportSignalBus(QObject):
    # path, dict_type, metadata, prompt, characters, settings, seed
    import_signal = Signal(str, dict, bool, bool, bool, bool)
    import_image_signal = Signal(str, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

# single shared bus
import_signal = ImportSignalBus()
