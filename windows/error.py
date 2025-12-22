from PySide6.QtWidgets import QPushButton, QLabel, QDialog, QGridLayout
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtCore import Qt

class Error(QDialog):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.text = text
        self.setWindowTitle("Error")
        self.build_error_window()
        self.exec()

    def build_error_window(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.error_label = QLabel(self.text, self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.error_label, 0, 0)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.close)  
        self.grid.addWidget(self.ok_button, 1, 0)

        
        


