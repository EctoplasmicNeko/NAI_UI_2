from PySide6.QtWidgets import QGridLayout, QFrame, QStackedWidget
from ui.columns.notebooks.character_notebook_tabs.character_lower_master_tab import CharacterLowerMasterTab



class CharacterLowerNotebook(QFrame):

    def __init__(self, parent, image_cache,):
        super().__init__(parent)
        self.setObjectName("character_lower_notebook")
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
        #---content frame --- row 1---    

        self.stack = QStackedWidget(self)
        self.grid.addWidget(self.stack, 1, 0)

        # build pages (could be real classes, not just empty QWidgets)
        self.character_tab_1 = CharacterLowerMasterTab(self, self.image_cache, 1) 
        self.character_tab_2 = CharacterLowerMasterTab(self, self.image_cache, 2)
        self.character_tab_3 = CharacterLowerMasterTab(self, self.image_cache, 3)
        self.character_tab_4 = CharacterLowerMasterTab(self, self.image_cache, 4)
        self.character_tab_5 = CharacterLowerMasterTab(self, self.image_cache, 5)

        self.stack.addWidget(self.character_tab_1)     # returns index 0
        self.stack.addWidget(self.character_tab_2)     # index 1
        self.stack.addWidget(self.character_tab_3)
        self.stack.addWidget(self.character_tab_4) 
        self.stack.addWidget(self.character_tab_5)      
        self.stack.setCurrentIndex(0)   # show page1





    
