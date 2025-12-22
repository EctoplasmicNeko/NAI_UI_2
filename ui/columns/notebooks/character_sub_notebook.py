from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QStackedWidget, QHBoxLayout, QPushButton, QButtonGroup, QSizePolicy
from ui.columns.notebooks.character_notebook_tabs.character_prompt_master_tab import CharacterPromptMasterTab
from ui.columns.notebooks.character_notebook_tabs.character_coordinate_tab import CharacterCoordinateTab
from ui.columns.notebooks.character_notebook_tabs.character_reference_master_tab import CharacterReferenceMasterTab
from ui.columns.notebooks.character_notebook_tabs.character_preset_tab import CharacterPresetTab
from ui.columns.notebooks.character_notebook_tabs.character_modifiers_tab import CharacterModifiersTab
from PySide6.QtCore import Qt


class CharacterSubNotebook(QFrame):

    def __init__(self, parent, image_cache, ID):
        super().__init__(parent)
        self.image_cache = image_cache
        self.ID = ID
        self.build_UI()
    
    def build_UI(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 1)

        #---button frame --- row 0---

        self.button_frame = QFrame(self)
        self.grid.addWidget(self.button_frame, 0, 0)

        self.button_frame_grid = QHBoxLayout(self.button_frame) 
        self.button_frame_grid.setContentsMargins(0,0,0,0) 
        self.button_frame_grid.setSpacing(0)
        self.button_frame_grid.setAlignment(Qt.AlignTop)
        self.button_frame_grid.setStretch(0,1)
        self.button_frame_grid.setStretch(1,1)

        self.button_1 = QPushButton("Prompt")
        self.button_frame_grid.addWidget(self.button_1)
        self.button_1.setCheckable(True) 
        self.button_1.setChecked(False)
        self.button_1.setMinimumWidth(5)
        self.button_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.button_2 = QPushButton("Grid")
        self.button_frame_grid.addWidget(self.button_2)
        self.button_2.setCheckable(True) 
        self.button_2.setChecked(False)
        self.button_2.setMinimumWidth(5)
        self.button_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.button_3 = QPushButton("Reference")
        self.button_frame_grid.addWidget(self.button_3)
        self.button_3.setCheckable(True) 
        self.button_3.setChecked(False)
        self.button_3.setMinimumWidth(5)
        self.button_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.button_4 = QPushButton("Modifiers")
        self.button_frame_grid.addWidget(self.button_4)
        self.button_4.setCheckable(True) 
        self.button_4.setChecked(False)
        self.button_4.setMinimumWidth(5)
        self.button_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.button_5 = QPushButton("Preset")
        self.button_frame_grid.addWidget(self.button_5)
        self.button_5.setCheckable(True) 
        self.button_5.setChecked(False)
        self.button_5.setMinimumWidth(5)
        self.button_5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)


        # Group them
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)          # exactly one can be checked at a time
        self.button_group.addButton(self.button_1, 0)             # optional: assign IDs for easy lookup
        self.button_group.addButton(self.button_2, 1)
        self.button_group.addButton(self.button_3, 2)
        self.button_group.addButton(self.button_4, 3)
        self.button_group.addButton(self.button_5, 4)


        #---content frame --- row 1---    

        self.stack = QStackedWidget(self)
        self.grid.addWidget(self.stack, 1, 0)

        # build pages (could be real classes, not just empty QWidgets)
        self.character_sub_tab_1 = CharacterPromptMasterTab(self)
        self.character_sub_tab_2 = CharacterCoordinateTab(self)
        self.character_sub_tab_3 = CharacterReferenceMasterTab(self,self.image_cache)
        self.character_sub_tab_4 = CharacterModifiersTab(self)
        self.character_sub_tab_5 = CharacterPresetTab(self, self.ID)
    

        self.stack.addWidget(self.character_sub_tab_1)     # returns index 0
        self.stack.addWidget(self.character_sub_tab_2)     # index 1
        self.stack.addWidget(self.character_sub_tab_3)
        self.stack.addWidget(self.character_sub_tab_4)
        self.stack.addWidget(self.character_sub_tab_5)

        self.button_1.setChecked(True)  # select button 1

        self.button_group.idToggled.connect(self.stack.setCurrentIndex)
