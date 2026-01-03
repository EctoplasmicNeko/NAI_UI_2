from PySide6.QtWidgets import QGridLayout, QFrame, QButtonGroup, QSizePolicy, QPushButton, QHBoxLayout, QStackedWidget, QWidget
from PySide6.QtCore import Qt
from ui.columns.notebooks.right_column_tabs. vibes_master_tab import VibeReferenceMasterTab

class RightColumn(QFrame):
    """Right column: same structure, ready for its own logic."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("right_column")
        self.build_right_column()

    def build_right_column(self):
       
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

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

        self.main_stack = QStackedWidget(self)
        self.grid.addWidget(self.main_stack, 1, 0)

        self.page0 = QWidget()
        self.page1 = VibeReferenceMasterTab(self)
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.page4 = QWidget()

        self.main_stack.addWidget(self.page0)
        self.main_stack.addWidget(self.page1)
        self.main_stack.addWidget(self.page2)
        self.main_stack.addWidget(self.page3)
        self.main_stack.addWidget(self.page4)
        
        self.button_group.idToggled.connect(self.main_stack.setCurrentIndex) #connect main stack



