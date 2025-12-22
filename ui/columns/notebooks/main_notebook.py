from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QStackedWidget, QHBoxLayout, QPushButton, QButtonGroup, QSizePolicy
from PySide6.QtCore import Qt
from ui.columns.notebooks.main_notebook_tabs.image_master_tab import ImageMasterTab
from ui.columns.notebooks.main_notebook_tabs.prompt_settings_tab import PromptSettingsTab
from ui.columns.notebooks.main_notebook_tabs.modifier_settings_tab import ModifierSettingsTab
from ui.columns.notebooks.main_notebook_tabs.program_settings_tab import ProgramSettingsTab
from ui.columns.notebooks.main_notebook_tabs.workflow_tab import WorkflowTab


class MainNotebook(QFrame):

    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.setObjectName("main_notebook")
        self.image_cache = image_cache
        self.build_UI()
        
    
    def build_UI(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 3, 0, 0)
        self.grid.setSpacing(3)
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 1)

        #---button frame --- row 0---

        self.button_frame = QFrame(self)
        self.button_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid.addWidget(self.button_frame, 0, 0)

        self.button_frame_grid = QHBoxLayout(self.button_frame) 
        self.button_frame_grid.setContentsMargins(0,0,0,0) 
        self.button_frame_grid.setSpacing(0)
        self.button_frame_grid.setAlignment(Qt.AlignTop)
        

        self.button_1 = QPushButton("Parameters")
        self.button_1.setCheckable(True) 
        self.button_1.setChecked(False)
        self.button_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.button_1.setMinimumWidth(5)
        self.button_frame_grid.addWidget(self.button_1)


        self.button_2 = QPushButton("Prompt")
        self.button_2.setCheckable(True) 
        self.button_2.setChecked(False)
        self.button_2.setMinimumWidth(5)
        self.button_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.button_frame_grid.addWidget(self.button_2)

        self.button_3 = QPushButton("Workflow")
        self.button_3.setCheckable(True) 
        self.button_3.setChecked(False)
        self.button_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.button_3.setMinimumWidth(5)
        self.button_frame_grid.addWidget(self.button_3)

        self.button_4 = QPushButton("Modifiers")
        self.button_4.setCheckable(True) 
        self.button_4.setChecked(False)
        self.button_4.setMinimumWidth(5)
        self.button_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.button_frame_grid.addWidget(self.button_4)

        self.button_5 = QPushButton("Settings")
        self.button_5.setCheckable(True) 
        self.button_5.setChecked(False)
        self.button_5.setMinimumWidth(5)
        self.button_5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.button_frame_grid.addWidget(self.button_5)

        # Group them
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)          # exactly one can be checked at a time
        self.button_group.addButton(self.button_1, 0)             # optional: assign IDs for easy lookup
        self.button_group.addButton(self.button_2, 1)
        self.button_group.addButton(self.button_3, 2)
        self.button_group.addButton(self.button_4, 3)
        self.button_group.addButton(self.button_5, 4)

        #---content frame --- row 1---    

        self.main_stack = QStackedWidget(self)
        self.grid.addWidget(self.main_stack, 1, 0)

        # build pages (could be real classes, not just empty QWidgets)
        self.page0 = ImageMasterTab(self) 
        self.page1 = PromptSettingsTab(self)
        self.page2 = WorkflowTab(self)
        self.page3 = ModifierSettingsTab(self)
        self.page4 = ProgramSettingsTab(self, self.image_cache)

        self.main_stack.addWidget(self.page0)     # returns index 0
        self.main_stack.addWidget(self.page1)     # index 1
        self.main_stack.addWidget(self.page2)
        self.main_stack.addWidget(self.page3) 
        self.main_stack.addWidget(self.page4)      
        
        self.button_1.setChecked(True)  # select button 1

        self.button_group.idToggled.connect(self.main_stack.setCurrentIndex)

