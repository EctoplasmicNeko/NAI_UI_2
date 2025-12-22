from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox
from data.datahub import get_data

class ImageGenerateSizesTab(QFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("image_generate_sizes_tab")
        self.build_image_generate_sizes_tab()
        self.update_size_properties()

    def build_image_generate_sizes_tab(self):
  
        self.sizes = get_data("sizes", [])                
        self.size_list = [f'{size["name"]} {size["image_height"]} x {size["image_width"]}' for size in self.sizes]
        self.size_list.insert(0, 'Custom Size')
        self.heights_list = [size['image_height'] for size in self.sizes]
        self.heights_list.insert(0, None)
        self.width_list = [size['image_width'] for size in self.sizes]
        self.width_list.insert(0, None)

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.sizes_comboxbox = QComboBox(self)
        self.sizes_comboxbox.addItems(self.size_list)
        self.sizes_comboxbox.currentIndexChanged.connect(self.update_size_properties)
        self.grid.addWidget(self.sizes_comboxbox, 0, 0)

    def update_size_properties(self):
        current_index = self.sizes_comboxbox.currentIndex()
        if current_index < 0:
            return
        self.sizes_comboxbox.setProperty('image_height', self.heights_list[current_index])
        print(self.sizes_comboxbox.property('image_height'))
        self.sizes_comboxbox.setProperty('image_width', self.width_list[current_index])

