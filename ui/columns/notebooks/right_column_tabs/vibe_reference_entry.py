from pathlib import Path

from PySide6.QtWidgets import QGridLayout, QFrame, QCheckBox, QLabel, QSizePolicy, QDoubleSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class VibeReferenceEntry(QFrame):

    def __init__(self, parent, image_path, image_name):
        super().__init__(parent)
        self.image_path = Path(image_path)
        self.image_name = image_name
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.build_vibe_reference_entry()

    def build_vibe_reference_entry(self):

        image_size = 160
        outer_margin = 10

        self.setFixedHeight(image_size + outer_margin * 2)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(outer_margin, outer_margin, outer_margin, outer_margin)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(6)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.image_label.setFixedSize(image_size, image_size)

        pixmap = QPixmap(str(self.image_path))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(image_size, image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)

        self.grid.addWidget(self.image_label, 0, 0, 3, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.use_vibe_checkbox = QCheckBox("Use Vibe", self)
        self.use_vibe_checkbox.setMinimumSize(24, 24)
        self.use_vibe_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.use_vibe_checkbox.setProperty("image_path", str(self.image_path))
        self.grid.addWidget(self.use_vibe_checkbox, 0, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.info_extracted_spinner = QDoubleSpinBox(self)
        self.info_extracted_spinner.setSingleStep(0.05)
        self.info_extracted_spinner.setDecimals(2)
        self.info_extracted_spinner.setRange(0.0, 1.0)
        self.info_extracted_spinner.setValue(1.0)
        self.info_extracted_spinner.setPrefix("Information: ")
        self.grid.addWidget(self.info_extracted_spinner, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.strength_spinner = QDoubleSpinBox(self)
        self.strength_spinner.setSingleStep(0.05)
        self.strength_spinner.setDecimals(2)
        self.strength_spinner.setRange(0.0, 10.0)
        self.strength_spinner.setValue(1.0)
        self.strength_spinner.setPrefix("Strength: ")
        self.grid.addWidget(self.strength_spinner, 2, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 1)
