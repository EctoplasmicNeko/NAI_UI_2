from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox, QCheckBox, QLabel, QScrollArea, QButtonGroup, QDoubleSpinBox, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from ui.columns.notebooks.character_notebook_tabs.character_reference_entry import CharacterReferenceEntry
from PySide6.QtWidgets import QGridLayout, QFrame, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt
...

class CharacterReferenceMasterTab(QFrame):

    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.image_cache = image_cache
        self.build_character_reference_master_tab()


    def build_character_reference_master_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.control_frame = QFrame(self)
        self.grid.addWidget(self.control_frame, 0, 0)

        self.control_frame_grid = QGridLayout(self.control_frame)
        self.control_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.control_frame_grid.setSpacing(0)
        self.control_frame_grid. setColumnStretch(0,0)
        self.control_frame_grid. setColumnStretch(1,1)

        self.enable_reference_checkbox = QCheckBox("Use References",self.control_frame)
        self.control_frame_grid.addWidget(self.enable_reference_checkbox, 0, 0)

        self.fidelity_spinner = QDoubleSpinBox(self.control_frame)
        self.fidelity_spinner.setSingleStep(0.05)
        self.fidelity_spinner.setDecimals(2)
        self.fidelity_spinner.setRange(0.0, 1.0)
        self.fidelity_spinner.setPrefix("Fidelity: ")
        self.control_frame_grid.addWidget(self.fidelity_spinner, 0, 1)

        self.style_aware_checkbox = QCheckBox("Style Aware", self.control_frame)
        self.control_frame_grid.addWidget(self.style_aware_checkbox, 1, 0)
        
        self.refstrength_spinner = QDoubleSpinBox(self.control_frame)
        self.refstrength_spinner.setSingleStep(0.05)
        self.refstrength_spinner.setDecimals(2)
        self.refstrength_spinner.setRange(0.0, 10.0)
        self.refstrength_spinner.setPrefix("Strength: ")
        self.control_frame_grid.addWidget(self.refstrength_spinner, 1, 1)

        self.subfolder_combobox = QComboBox(self.control_frame)
        self.control_frame_grid.addWidget(self.subfolder_combobox, 2, 0,)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QFrame(self.scroll_area)
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_area.setWidget(self.scroll_content)

        self.references_grid = QGridLayout(self.scroll_content)
        self.references_grid.setContentsMargins(4, 4, 4, 4)
        self.references_grid.setVerticalSpacing(8)
        self.references_grid.setHorizontalSpacing(0)

        # ⬅️ Make column 0 (the card column) fill the width
        self.references_grid.setColumnStretch(0, 1)

        self.grid.addWidget(self.scroll_area, 1, 0)

        self.reference_button_group = QButtonGroup(self)
        self.reference_button_group.setExclusive(True)

        self.subfolder_combobox.currentIndexChanged.connect(self.on_subfolder_changed)


        # --- pretty vertical scrollbar ---


    def rebuild_character_references(self, character_name):

        # --- clear existing entries / old stack from main grid ---
        for i in reversed(range(self.references_grid.count())):
            item = self.references_grid.takeAt(i)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # --- clear existing buttons from the group ---
        for btn in self.reference_button_group.buttons():
            self.reference_button_group.removeButton(btn)

        # --- reset subfolder combo ---
        self.subfolder_combobox.blockSignals(True)
        self.subfolder_combobox.clear()
        self.subfolder_combobox.blockSignals(False)

        # --- always recreate the stacked widget and put it back in the grid ---
        self.reference_stack = QStackedWidget(self.scroll_content)
        self.references_grid.addWidget(self.reference_stack, 0, 0)

        # --- get this character's data ---
        char_dict = self.image_cache['references'].get(character_name)

        # if no references at all, show a placeholder page so the stack still exists
        if not char_dict:
            placeholder_page = QFrame(self.reference_stack)
            placeholder_layout = QVBoxLayout(placeholder_page)
            placeholder_layout.setContentsMargins(4, 4, 4, 4)
            placeholder_layout.setSpacing(8)

            msg = QLabel("No reference images for this character.", placeholder_page)
            msg.setAlignment(Qt.AlignCenter)
            placeholder_layout.addWidget(msg)
            placeholder_layout.addStretch(1)

            idx = self.reference_stack.addWidget(placeholder_page)
            self.subfolder_combobox.addItem("(None)", idx)
            self.reference_stack.setCurrentIndex(0)
            return

        # --- split into real subfolders and root-level images ---
        subfolders = {}
        root_images = {}

        for key, value in char_dict.items():
            if isinstance(value, dict):
                subfolders[key] = value
            else:
                root_images[key] = value

        if root_images:
            subfolders["(Root)"] = root_images

        button_id = 0  # id for QButtonGroup

        for subfolder_name, images_dict in subfolders.items():
            page = QFrame(self.reference_stack)
            page_layout = QVBoxLayout(page)
            page_layout.setContentsMargins(4, 4, 4, 4)
            page_layout.setSpacing(8)

            for image_name, image_path in images_dict.items():
                entry = CharacterReferenceEntry(page, image_path, image_name)
                page_layout.addWidget(entry)

                self.reference_button_group.addButton(entry.use_reference_checkbox, button_id)
                button_id += 1

            page_layout.addStretch(1)

            index = self.reference_stack.addWidget(page)
            self.subfolder_combobox.addItem(subfolder_name, index)

        if self.subfolder_combobox.count() > 0:
            self.reference_stack.setCurrentIndex(0)


    def on_subfolder_changed(self, index):
        if index < 0:
            return
        stack_index = self.subfolder_combobox.itemData(index)
        if stack_index is not None:
            self.reference_stack.setCurrentIndex(stack_index)