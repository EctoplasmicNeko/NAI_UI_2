from PySide6.QtWidgets import QGridLayout, QFrame,QComboBox


class ImageRequestsTab(QFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_requests_tab()

    def build_image_requests_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(3)

        self.request_combobox = QComboBox()
        self.request_combobox.addItems(["Generate", "Emotion", "Colorize"])
        self.grid.addWidget(self.request_combobox, 0, 0)