from PySide6.QtWidgets import QFrame, QGridLayout, QSizePolicy, QToolButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from process.CompletionSignaler import completion_signaler

class CentreColumn(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("centre_column")
        self.current_image_path = None
        completion_signaler.window_lock_signal.connect(lambda locked: self.viewport_button.blockSignals(locked))
        completion_signaler.complete_signal.connect(lambda: self.viewport_button.blockSignals(False))
        self.build_centre_column()


    def build_centre_column(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.grid.setColumnStretch(0, 1)
        self.grid.setRowStretch(0, 1)
        self.viewport_button = QToolButton(self)
        self.viewport_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.viewport_button.setCursor(Qt.PointingHandCursor)
        self.viewport_button.setToolTip("Generate image")
        self.viewport_button.setAutoRaise(True)
        self.viewport_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.viewport_button.setLayoutDirection(Qt.LeftToRight)

        self.grid.addWidget(self.viewport_button, 0, 0)

    def update_image(self, image_path):
        self.current_image_path = image_path
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            return

        self.viewport_button.updateGeometry()

        label_width = self.viewport_button.width()
        label_height = self.viewport_button.height()

        image_width = pixmap.width()
        image_height = pixmap.height()

        # Only reduce size, never enlarge
        if image_width > label_width or image_height > label_height:
            pixmap = pixmap.scaled(
                label_width,
                label_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

        self.viewport_button.setIcon(QIcon(pixmap))
        self.viewport_button.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.viewport_button.setAutoRepeat
        self.viewport_button.setAutoRepeatDelay(300)
        self.viewport_button.setAutoRepeatInterval(100)

        

        
        