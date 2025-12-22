from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PySide6.QtCore import Qt


class Confirm(QDialog):
    def __init__(self, parent, title, text, true_text="Yes", false_text="No"):
        super().__init__(parent)
        self.text = text
        self.true_text = true_text
        self.false_text = false_text

        self.setWindowTitle(title)
        self.build_confirm_window()

    def build_confirm_window(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(8, 8, 8, 8)
        self.grid.setSpacing(8)

        # Text
        self.text_label = QLabel(self.text, self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.text_label, 0, 0)

        # Button frame
        self.button_frame = QFrame(self)
        self.button_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.button_frame_grid = QGridLayout(self.button_frame)
        self.button_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.button_frame_grid.setSpacing(6)

        self.grid.addWidget(self.button_frame, 1, 0, alignment=Qt.AlignCenter)

        # True / false buttons
        self.true_button = QPushButton(self.true_text, self)
        self.true_button.clicked.connect(self.accept)   # dialog result = Accepted
        self.button_frame_grid.addWidget(self.true_button, 0, 0)

        self.false_button = QPushButton(self.false_text, self)
        self.false_button.clicked.connect(self.reject)  # dialog result = Rejected
        self.button_frame_grid.addWidget(self.false_button, 0, 1)
