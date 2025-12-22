from PySide6.QtWidgets import QGridLayout, QFrame, QStackedWidget
from ui.columns.notebooks.main_notebook_tabs.image_generate_master_tab import ImageGenerateMasterTab
from ui.columns.notebooks.main_notebook_tabs.image_requests_tab import ImageRequestsTab
from ui.columns.notebooks.main_notebook_tabs.image_augment_emotion_tab import ImageAugmentEmotionTab
from ui.columns.notebooks.main_notebook_tabs.image_augment_colorize_tab import ImageAugmentColorizeTab


class ImageMasterTab(QFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_requests_tab()

    def build_image_requests_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 3, 0, 0)
        self.grid.setSpacing(0)

        self.requests_tab = ImageRequestsTab(self)
        self.grid.addWidget(self.requests_tab, 0, 0)

        self.image_master_stack = QStackedWidget(self)
        self.grid.addWidget(self.image_master_stack, 1, 0)

        # build pages (could be real classes, not just empty QWidgets)
        self.image_master_stack_generate = ImageGenerateMasterTab(self) 
        self.image_master_stack_emotion = ImageAugmentEmotionTab(self) 
        self.image_master_stack_colorize = ImageAugmentColorizeTab(self)

        self.image_master_stack.addWidget(self.image_master_stack_generate)     # returns index 0
        self.image_master_stack.addWidget(self.image_master_stack_emotion)     # index 1
        self.image_master_stack.addWidget(self.image_master_stack_colorize)     # index 2
        self.image_master_stack.setCurrentIndex(0)   # show page1

        self.requests_tab.request_combobox.currentIndexChanged.connect(self.image_master_stack.setCurrentIndex)




