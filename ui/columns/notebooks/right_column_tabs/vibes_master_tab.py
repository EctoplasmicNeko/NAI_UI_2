from pathlib import Path

from PySide6.QtWidgets import (
    QGridLayout, QFrame, QCheckBox, QLabel, QSizePolicy,
    QVBoxLayout, QScrollArea, QComboBox
)
from PySide6.QtCore import Qt

from ui.columns.notebooks.right_column_tabs.vibe_reference_entry import VibeReferenceEntry
from data.paths import USER_DIR


class VibeReferenceMasterTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.vibes_root_dir = USER_DIR / "vibes"
        self.vibes_root_dir.mkdir(parents=True, exist_ok=True)

        self.current_page_widget = None
        self.current_page_layout = None
        self.pages = []

        self.build_vibe_reference_master_tab()
        self.refresh_vibe_pages()

    def build_vibe_reference_master_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # --- control frame ---
        self.control_frame = QFrame(self)
        self.grid.addWidget(self.control_frame, 0, 0)

        self.control_frame_grid = QGridLayout(self.control_frame)
        self.control_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.control_frame_grid.setHorizontalSpacing(8)
        self.control_frame_grid.setVerticalSpacing(6)
        self.control_frame_grid.setColumnStretch(0, 0)
        self.control_frame_grid.setColumnStretch(1, 1)

        self.enable_vibes_checkbox = QCheckBox("Use Vibes", self.control_frame)
        self.control_frame_grid.addWidget(self.enable_vibes_checkbox, 0, 0, 1, 2)

        self.normalize_strength_checkbox = QCheckBox("Normalize Strengths", self.control_frame)
        self.control_frame_grid.addWidget(self.normalize_strength_checkbox, 1, 0, 1, 2)

        self.subfolder_combobox = QComboBox(self.control_frame)
        self.control_frame_grid.addWidget(self.subfolder_combobox, 2, 0, 1, 2)

        # --- scroll area ---
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QFrame(self.scroll_area)
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_area.setWidget(self.scroll_content)

        self.vibes_grid = QGridLayout(self.scroll_content)
        self.vibes_grid.setContentsMargins(4, 4, 4, 4)
        self.vibes_grid.setVerticalSpacing(8)
        self.vibes_grid.setHorizontalSpacing(0)
        self.vibes_grid.setColumnStretch(0, 1)

        self.grid.addWidget(self.scroll_area, 1, 0)

        self.subfolder_combobox.currentIndexChanged.connect(self.on_subfolder_changed)

    def refresh_vibe_pages(self):

        self.subfolder_combobox.blockSignals(True)
        self.subfolder_combobox.clear()
        self.subfolder_combobox.blockSignals(False)

        if self.current_page_widget is not None:
            self.vibes_grid.removeWidget(self.current_page_widget)
            self.current_page_widget.setVisible(False)
            self.current_page_widget = None
            self.current_page_layout = None

        for name, page in self.pages:
            page.deleteLater()
        self.pages.clear()

        subfolders = {}
        root_images = []

        for item in sorted(self.vibes_root_dir.iterdir()):
            if item.is_dir():
                images = self.collect_images_from_folder(item)
                if images:
                    subfolders[item.name] = images
            elif item.is_file() and item.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                root_images.append(item)

        if root_images:
            subfolders["(Root)"] = sorted(root_images)

        if not subfolders:
            placeholder = QFrame(self.scroll_content)
            layout = QVBoxLayout(placeholder)
            layout.setContentsMargins(4, 4, 4, 4)

            msg = QLabel("No vibe images found.", placeholder)
            msg.setAlignment(Qt.AlignCenter)
            layout.addWidget(msg)
            layout.addStretch(1)

            self.set_current_page(placeholder, layout)
            self.subfolder_combobox.addItem("(None)", "(None)")
            return

        for subfolder_name, image_paths in subfolders.items():
            page = QFrame(self.scroll_content)
            layout = QVBoxLayout(page)
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setSpacing(8)

            for image_path in image_paths:
                entry = VibeReferenceEntry(page, image_path, image_path.name)
                layout.addWidget(entry)

            layout.addStretch(1)

            self.pages.append((subfolder_name, page))
            self.subfolder_combobox.addItem(subfolder_name, subfolder_name)

        self.subfolder_combobox.blockSignals(True)
        self.subfolder_combobox.setCurrentIndex(0)
        self.subfolder_combobox.blockSignals(False)
        self.on_subfolder_changed(0)

    def collect_images_from_folder(self, folder_path):

        images = []
        for item in sorted(folder_path.rglob("*")):
            if item.is_file() and item.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                images.append(item)
        return images

    def set_current_page(self, page_widget, page_layout):

        self.current_page_widget = page_widget
        self.current_page_layout = page_layout
        self.vibes_grid.addWidget(self.current_page_widget, 0, 0)
        self.current_page_widget.setVisible(True)

    def on_subfolder_changed(self, index):

        if index < 0:
            return

        subfolder_name = self.subfolder_combobox.itemData(index)
        if not subfolder_name:
            return

        if self.current_page_widget is not None:
            self.vibes_grid.removeWidget(self.current_page_widget)
            self.current_page_widget.setVisible(False)
            self.current_page_widget = None
            self.current_page_layout = None

        for name, page in self.pages:
            if name == subfolder_name:
                self.set_current_page(page, page.layout())
                break

    def export_state(self):

        reference_image_paths = []
        reference_strengths = []
        reference_information_extracted = []

        if self.current_page_layout is None:
            return reference_image_paths, reference_strengths, reference_information_extracted

        for i in range(self.current_page_layout.count()):
            widget = self.current_page_layout.itemAt(i).widget()
            if not isinstance(widget, VibeReferenceEntry):
                continue
            if not widget.use_vibe_checkbox.isChecked():
                continue

            reference_image_paths.append(str(widget.image_path))
            reference_strengths.append(round(widget.strength_spinner.value(), 2))
            reference_information_extracted.append(round(widget.info_extracted_spinner.value(), 2))


        return {
            "reference_image_paths": reference_image_paths,
            "reference_strengths": reference_strengths,
            "reference_information_extracted": reference_information_extracted,
            "normalize_strength": self.normalize_strength_checkbox.isChecked(),
            "vibe_enabled": self.enable_vibes_checkbox.isChecked(),
        }