from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QStackedWidget, QHBoxLayout, QPushButton, QButtonGroup, QSizePolicy
from PySide6.QtCore import Qt
from ui.columns.notebooks.character_notebook_tabs.character_middle_master_tab import CharacterMiddleMasterTab



class CharacterMiddleNotebook(QFrame):

    def __init__(self, parent, image_cache,):
        super().__init__(parent)
        self.setObjectName("character_middle_notebook")
        self.image_cache = image_cache
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
        self.button_frame_grid.setStretch(2,1)
        self.button_frame_grid.setStretch(3,1)
        self.button_frame_grid.setStretch(4,1)


        self.button_name_1 = "Character 1"
        self.button_1 = QPushButton(self.button_name_1)
        self.button_frame_grid.addWidget(self.button_1)
        self.button_1.setCheckable(True) 
        self.button_1.setChecked(False)
        self.button_1.setMinimumWidth(5)
        self.button_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        

        self.button_name_2 = "Character 2"
        self.button_2 = QPushButton(self.button_name_2)
        self.button_frame_grid.addWidget(self.button_2)
        self.button_2.setCheckable(True) 
        self.button_2.setChecked(False)
        self.button_2.setMinimumWidth(5)
        self.button_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        

        self.button_name_3 = "Character 3"
        self.button_3 = QPushButton(self.button_name_3)
        self.button_frame_grid.addWidget(self.button_3)
        self.button_3.setCheckable(True) 
        self.button_3.setChecked(False)
        self.button_3.setMinimumWidth(5)
        self.button_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        

        self.button_name_4 = "Character 4"
        self.button_4 = QPushButton(self.button_name_4)
        self.button_frame_grid.addWidget(self.button_4)
        self.button_4.setCheckable(True) 
        self.button_4.setChecked(False)
        self.button_4.setMinimumWidth(5)
        self.button_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        

        self.button_name_5 = "Character 5"
        self.button_5 = QPushButton(self.button_name_5)
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
        self.character_tab_1 = CharacterMiddleMasterTab(self, self.image_cache, 1) 
        self.character_tab_2 = CharacterMiddleMasterTab(self, self.image_cache, 2)
        self.character_tab_3 = CharacterMiddleMasterTab(self, self.image_cache, 3)
        self.character_tab_4 = CharacterMiddleMasterTab(self, self.image_cache, 4)
        self.character_tab_5 = CharacterMiddleMasterTab(self, self.image_cache, 5)

        self.character_tab_1.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.update_tab_for_character(self.button_1, self.character_tab_1, '1'))
        self.character_tab_2.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.update_tab_for_character(self.button_2, self.character_tab_2, '2'))
        self.character_tab_3.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.update_tab_for_character(self.button_3, self.character_tab_3, '3'))
        self.character_tab_4.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.update_tab_for_character(self.button_4, self.character_tab_4, '4'))
        self.character_tab_5.fluff_tab.character_select_combobox.currentIndexChanged.connect(lambda: self.update_tab_for_character(self.button_5, self.character_tab_5, '5'))

        self.stack.addWidget(self.character_tab_1)     # returns index 0
        self.stack.addWidget(self.character_tab_2)     # index 1
        self.stack.addWidget(self.character_tab_3)
        self.stack.addWidget(self.character_tab_4) 
        self.stack.addWidget(self.character_tab_5)      
        self.stack.setCurrentIndex(0)   # show page1
        self.button_1.setChecked(True)  # select button 1

        self.button_group.idToggled.connect(self.stack.setCurrentIndex)
    

    def update_tab_for_character(self, button, cha_tab, button_num):
        name = cha_tab.fluff_tab.character_select_combobox.currentText()
        if name != "None":
            button.setText (name)
        else:
            button.setText (f'Character {button_num}')



    
