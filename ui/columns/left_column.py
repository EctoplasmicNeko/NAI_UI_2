
from PySide6.QtWidgets import QGridLayout, QFrame
from ui.columns.notebooks.main_notebook import MainNotebook
from ui.columns.notebooks.character_lower_notebook import CharacterLowerNotebook
from ui.columns.notebooks.character_middle_notebook import CharacterMiddleNotebook
from data.datahub import get_all_characters
from signaling.refresh_character_lists import refresh_character_lists_signal

class LeftColumn(QFrame):
    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.setObjectName("left_column")
        self.image_cache = image_cache
        self.characters = get_all_characters()
        self.build_left_column()
        self.upper_frame.page4.character_sorting_combo.currentIndexChanged.connect(self.refresh_all_character_lists)
        refresh_character_lists_signal.refresh_lists.connect(self.refresh_all_character_lists)

    def build_left_column(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(5, 5, 5, 5)
        self.grid.setSpacing(5)

        self.grid.setRowStretch(0,50)
        self.grid.setRowStretch(1,0)
        self.grid.setRowStretch(2,50)

        self.upper_frame = MainNotebook(self, self.image_cache)
        self.grid.addWidget(self.upper_frame, 0, 0)

        self.middle_frame = CharacterMiddleNotebook(self, self.image_cache)
        self.grid.addWidget(self.middle_frame, 1, 0)

        self.lower_frame = CharacterLowerNotebook(self, self.image_cache)
        self.grid.addWidget(self.lower_frame, 2, 0)

        self.middle_frame.button_group.idToggled.connect(self.lower_frame.stack.setCurrentIndex) #connect character notebooks

    def refresh_all_character_lists(self):
        print("Refreshing character lists...")   
        self.characters = get_all_characters()
        self.character_list = self.get_sorted_characters_by_priority()

        self.middle_frame.character_tab_1.characters = self.characters
        self.middle_frame.character_tab_1.fluff_tab.characters = self.characters
        self.middle_frame.character_tab_1.character_list = self.character_list
        self.middle_frame.character_tab_1.on_refresh_character_list()
        self.lower_frame.character_tab_1.characters = self.characters
        self.lower_frame.character_tab_1.character_autocycle_manager.base_character_list = self.character_list
        self.lower_frame.character_tab_1.on_refresh_character_list()

        self.middle_frame.character_tab_2.characters = self.characters
        self.middle_frame.character_tab_2.fluff_tab.characters = self.characters
        self.middle_frame.character_tab_2.character_list = self.character_list
        self.middle_frame.character_tab_2.on_refresh_character_list()
        self.lower_frame.character_tab_2.characters = self.characters
        self.lower_frame.character_tab_2.character_autocycle_manager.base_character_list = self.character_list
        self.lower_frame.character_tab_2.on_refresh_character_list()

        self.middle_frame.character_tab_3.characters = self.characters
        self.middle_frame.character_tab_3.fluff_tab.characters = self.characters
        self.middle_frame.character_tab_3.character_list = self.character_list
        self.middle_frame.character_tab_3.on_refresh_character_list()
        self.lower_frame.character_tab_3.characters = self.characters
        self.lower_frame.character_tab_3.character_autocycle_manager.base_character_list = self.character_list
        self.lower_frame.character_tab_3.on_refresh_character_list()

        self.middle_frame.character_tab_4.characters = self.characters
        self.middle_frame.character_tab_4.fluff_tab.characters = self.characters
        self.middle_frame.character_tab_4.character_list = self.character_list
        self.middle_frame.character_tab_4.on_refresh_character_list()
        self.lower_frame.character_tab_4.characters = self.characters
        self.lower_frame.character_tab_4.character_autocycle_manager.base_character_list = self.character_list
        self.lower_frame.character_tab_4.on_refresh_character_list()

        self.middle_frame.character_tab_5.characters = self.characters
        self.middle_frame.character_tab_5.fluff_tab.characters = self.characters
        self.middle_frame.character_tab_5.character_list = self.character_list
        self.middle_frame.character_tab_5.on_refresh_character_list()
        self.lower_frame.character_tab_5.characters = self.characters
        self.lower_frame.character_tab_5.character_autocycle_manager.base_character_list = self.character_list
        self.lower_frame.character_tab_5.on_refresh_character_list()


    def get_character_priority_score(self, character_dict):
        sort_type = self.upper_frame.page4.character_sorting_combo.currentText()

        if sort_type == "Status":
            tags = character_dict.get("tags", [])
            if not isinstance(tags, list):
                return 0
            if "Main" in tags:
                return 3
            if "Supporting" in tags:
                return 2
            if "Minor" in tags:
                return 1
            return 0

        if sort_type in ("Youngest", "Oldest"):
            age = character_dict.get("age", None)
            try:
                age_int = int(age)
            except (TypeError, ValueError):
                age_int = 10**9  # unknown ages sink to the bottom
            return -age_int if sort_type == "Youngest" else age_int

        # Alphabetical doesn't need a numeric score
        return 0

    def get_sorted_characters_by_priority(self):
            sort_type = self.upper_frame.page4.character_sorting_combo.currentText()

            if sort_type == "Alphabetical":
                return sorted((c.get("nameID","") for c in self.characters), key=str.lower)

            sorted_chars = sorted(self.characters, key=lambda c: (-self.get_character_priority_score(c), str(c.get("nameID","")).lower()))
            return [c.get("nameID","") for c in sorted_chars]




    


       