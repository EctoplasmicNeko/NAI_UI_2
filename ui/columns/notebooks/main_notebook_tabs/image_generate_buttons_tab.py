from PySide6.QtWidgets import QGridLayout, QFrame, QCheckBox


class ImageGenerateButtonsTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("image_generate_buttons_tab")
        self.build_image_generate_buttons_tab()

    def build_image_generate_buttons_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(5)
    
        self.legacy_v3_checkbox = QCheckBox("Legacy V3")
        self.grid.addWidget(self.legacy_v3_checkbox, 0, 0)

        self.legacy_v4_checkbox = QCheckBox("Legacy V4")
        self.grid.addWidget(self.legacy_v4_checkbox, 0, 1)

        self.SMEA_checkbox = QCheckBox("SMEA")
        self.SMEA_checkbox.checkStateChanged.connect(self.update_DYN_for_SMEA)
        self.grid.addWidget(self.SMEA_checkbox, 0, 2)

        self.DYN_checkbox = QCheckBox("DYN")
        self.grid.addWidget(self.DYN_checkbox, 0, 3)

        self.variety_checkbox = QCheckBox("Variety+")
        self.grid.addWidget(self.variety_checkbox, 1, 0)

        self.decrisp_checkbox = QCheckBox("Decrisp")
        self.grid.addWidget(self.decrisp_checkbox, 1, 1)

        self.brownian_checkbox = QCheckBox("Brownian")
        self.grid.addWidget(self.brownian_checkbox, 1, 2)

    def update_DYN_for_SMEA(self):
        if self.SMEA_checkbox.isChecked():
            self.DYN_checkbox.setEnabled(True)
        else:
            self.DYN_checkbox.setEnabled(False)
