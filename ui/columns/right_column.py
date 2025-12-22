from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from ui.columns.notebooks.main_notebook import MainNotebook
from ui.columns.notebooks.character_lower_notebook import CharacterLowerNotebook

class RightColumn(QFrame):
    """Right column: same structure, ready for its own logic."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("right_column")
        self.build_right_column()

    def build_right_column(self):
       
        self.grid = QVBoxLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)



