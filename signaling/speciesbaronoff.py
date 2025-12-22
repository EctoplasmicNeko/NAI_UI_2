from PySide6.QtCore import QObject, Signal

class SpeciesBarOnOff(QObject):
    on_signal = Signal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)

species_bar_on_off = SpeciesBarOnOff()