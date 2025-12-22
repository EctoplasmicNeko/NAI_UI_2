from PySide6.QtWidgets import QGridLayout, QFrame, QCheckBox, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class CharacterReferenceEntry(QFrame):

    def __init__(self, parent, image_path, image_name):
        super().__init__(parent)
        self.image_path = image_path
        self.image_name = image_name
    
        # expand horizontally, fixed-ish vertically
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.build_character_reference()

    def build_character_reference(self):

        image_size = 160
        outer_margin = 10

        self.setFixedHeight(image_size + outer_margin * 2)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(outer_margin, outer_margin, outer_margin, outer_margin)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(0)

        # --- image (col 0) ---
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.image_label.setFixedSize(image_size, image_size)

        pix = QPixmap(str(self.image_path))
        if not pix.isNull():
            pix = pix.scaled(
                image_size,
                image_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.image_label.setPixmap(pix)

        self.grid.addWidget(self.image_label, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)


        # --- checkbox (col 2) ---
        self.use_reference_checkbox = QCheckBox('Use Reference', self)
        self.use_reference_checkbox.setMinimumSize(24, 24)
        self.use_reference_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.use_reference_checkbox.setProperty('image_path', self.image_path)

        self.grid.addWidget(self.use_reference_checkbox, 0, 1,
                            Qt.AlignLeft | Qt.AlignVCenter)

        # image and checkbox columns don't stretch
        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 1)
