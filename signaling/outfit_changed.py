from PySide6.QtCore import QObject, Signal

class OutfitChangedSignal(QObject):
    outfit_changed = Signal(str, int)   # send just the outfit name

outfit_changed_signal = OutfitChangedSignal()
