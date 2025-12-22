from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from signaling.minimal_character_tab import minimal_character_tab
from data.datahub import get_all_characters


class CharacterFluffTab(QFrame):
    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.image_cache = image_cache
        self.build_character_fluff_tab()
        minimal_character_tab.on_signal.connect(self.minimal_character_fluff_tab)
        

    def build_character_fluff_tab(self):

        self.characters = get_all_characters()                
        self.character_list = [f'{character["nameID"]}' for character in self.characters]

        # ---- Base layout ----
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(3)
        self.grid.setColumnStretch(0,1)
        self.grid.setColumnStretch(1,0)
        self.grid.setRowStretch(1,0)



        # ---- Left text block ----
        self.character_select_combobox = QComboBox(self)
        self.character_select_combobox.addItem("None")
        self.character_select_combobox.addItems(self.character_list)
        self.character_select_combobox.setEditable(False)
        self.grid.addWidget(self.character_select_combobox,0, 0)

        self.character_fluff_frame = QFrame(self)
        self.character_fluff_frame_grid = QGridLayout(self.character_fluff_frame)
        self.character_fluff_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.character_fluff_frame_grid.setSpacing(3)
        self.grid.addWidget(self.character_fluff_frame, 1, 0)    

        self.character_fluff_fullname_label = QLabel(self)
        self.character_fluff_fullname_label.setWordWrap(True)
        self.character_fluff_fullname_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_fluff_fullname_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_frame_grid.addWidget(self.character_fluff_fullname_label, 0, 0, )

        self.character_fluff_species_label = QLabel(self)
        self.character_fluff_species_label.setWordWrap(True)
        self.character_fluff_species_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_fluff_species_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_frame_grid.addWidget(self.character_fluff_species_label, 1,0 )

        self.character_fluff_subspecies_label = QLabel(self)
        self.character_fluff_subspecies_label.setWordWrap(True)
        self.character_fluff_subspecies_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_fluff_subspecies_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_frame_grid.addWidget(self.character_fluff_subspecies_label, 2,0 )

        self.character_fluff_age_label = QLabel(self)
        self.character_fluff_age_label.setWordWrap(True)
        self.character_fluff_age_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_fluff_age_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_frame_grid.addWidget(self.character_fluff_age_label, 3,0 )

        self.character_fluff_gender_label = QLabel(self)
        self.character_fluff_gender_label.setWordWrap(True)
        self.character_fluff_gender_label.setTextFormat(Qt.RichText)
        self.character_fluff_gender_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_fluff_gender_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_frame_grid.addWidget(self.character_fluff_gender_label, 4,0 )


        self.character_portrait_frame = QFrame(self)
        self.character_portrait_frame.setMinimumSize(170, 170)
        self.character_portrait_frame_grid = QVBoxLayout(self.character_portrait_frame)
        self.character_portrait_frame.setContentsMargins(6, 6, 6, 6)
        self.character_portrait_frame_grid.setSpacing(4)
        self.grid.addWidget(self.character_portrait_frame, 0, 1, 2, 1)

        self.character_fluff_quote_label = QLabel(self)
        self.character_fluff_quote_label.setWordWrap(True)
        self.character_fluff_quote_label.setTextFormat(Qt.RichText)
        self.character_fluff_quote_label.setAlignment(Qt.AlignCenter)
        self.character_fluff_quote_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.character_fluff_quote_label.setMinimumHeight(25)
        self.grid.addWidget(self.character_fluff_quote_label, 2,0, 1, 2 )

        # === portrait label (keep as attribute!) ===
        self.portrait_label = QLabel(self.character_portrait_frame)
        self.portrait_label.setAlignment(Qt.AlignCenter)
        self.portrait_label.setFixedSize(150, 150)
        self.character_portrait_frame_grid.addWidget(self.portrait_label, 0, Qt.AlignCenter)

    def update_portrait(self, path: str):
        """Load and apply a rounded portrait from the given file path."""
        self.pix_path = path
        if self.pix_path == "":
            self.pix_path = self.image_cache['character_portraits']['fluff_placeholder']

        pix = QPixmap(self.pix_path)
        pix = pix.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.portrait_label.setPixmap(pix)

    def minimal_character_fluff_tab(self, enabled: bool):
        if enabled:
            self.character_fluff_frame.show()
            self.character_portrait_frame.show()
        else:
            self.character_fluff_frame.hide()
            self.character_portrait_frame.hide()





