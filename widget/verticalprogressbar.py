from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QRect

class VerticalTextProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)
        self.setTextVisible(True)   # we’ll ignore Qt's text painting and draw our own

    def paintEvent(self, event):
        # 1. Let the base class draw the bar (but with no text)
        original_text_visible = self.isTextVisible()
        self.setTextVisible(False)
        super().paintEvent(event)
        self.setTextVisible(original_text_visible)

        # 2. Draw rotated text on top
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        text = self.text() or f"{self.value()}%"

        # Move origin to bottom-left, then rotate so text runs along the bar
        painter.translate(0, self.height())
        painter.rotate(-90)

        # After rotating, the logical rect is height x width
        text_rect = QRect(0, 0, self.height(), self.width())
        painter.drawText(text_rect, Qt.AlignCenter, text)

        painter.end()
