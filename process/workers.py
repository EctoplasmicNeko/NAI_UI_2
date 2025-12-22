from PySide6.QtCore import QObject, Signal
from data.save import save_config
from process.process_main import run_process


class GenerateWorker(QObject):
    finished = Signal()
    result = Signal(str, dict)   # image_path, state

    def __init__(self, state):
        super().__init__()
        self.state = state

    def run(self):
        save_config(self.state)
        image_path = run_process(self.state)
        self.result.emit(image_path, self.state)
        self.finished.emit()
