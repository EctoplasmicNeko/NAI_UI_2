
from PySide6.QtCore import QObject, Signal

class CompletionSignaler(QObject):
    start_signal = Signal()
    complete_signal = Signal()
    loop_start_signal = Signal(str)
    loop_complete_signal = Signal()
    set_start_signal = Signal()
    set_complete_signal = Signal()
    window_lock_signal = Signal(bool)
      
    def __init__(self, parent = None):
        super().__init__(parent)

completion_signaler = CompletionSignaler()