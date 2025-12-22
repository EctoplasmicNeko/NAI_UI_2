from PySide6.QtWidgets import QGridLayout, QFrame, QDoubleSpinBox, QLabel
from PySide6.QtCore import Qt, Signal


class CharacterQuickTab(QFrame):
    # character_name, quick_weights_data
    quickWeightsChanged = Signal(str, list)

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("character_quick_tab")
        self.quick_weights_data = []
        self.current_character_name = None
        self.build_character_quick_tab()
        self.setMinimumHeight(70)
        
    def build_character_quick_tab(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)    
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 0)
        self.grid.setRowStretch(2, 1) 

        self.quick_tab_label = QLabel("Quick Weights", self)
        self.quick_tab_label.setObjectName("quick_tab_label")
        self.quick_tab_label.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.quick_tab_label, 0, 0, 1, 2)

        self.spinner_frame = QFrame(self)
        self.spinner_grid = QGridLayout(self.spinner_frame)
        self.spinner_grid.setContentsMargins(4, 4, 4, 4)
        self.spinner_grid.setSpacing(4)
        self.grid.addWidget(self.spinner_frame, 1, 0, 1, 2)

    def rebuild_quick_weights(self, character_name, quick_weights_data):
        self.current_character_name = character_name
        self.quick_weights_data = quick_weights_data or []

        # clear existing contents in spinner_grid (but keep the layout itself)
        while self.spinner_grid.count():
            item = self.spinner_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        # if no quick weights, show placeholder
        if not self.quick_weights_data:
            placeholder_label = QLabel("Character has no assigned quick weights", self.spinner_frame)
            placeholder_label.setAlignment(Qt.AlignCenter)
            # span both columns so it stays centered nicely
            self.spinner_grid.addWidget(placeholder_label, 0, 0, 2, 2)
            return

        # otherwise, build spinners
        row = 0
        column = 0

        for quick_weight in self.quick_weights_data:
            spinner = QDoubleSpinBox(self.spinner_frame)
            
            spinner.setPrefix(f"{quick_weight['tag']}: ")
            spinner.setProperty("tag", quick_weight['tag'])
            spinner.setProperty("negative", quick_weight['negative'])
            spinner.setRange(quick_weight['min'], quick_weight['max'])
            spinner.setDecimals(1)          # 1 decimal place in UI
            spinner.setSingleStep(0.1)     # move in 0.1 steps
            spinner.lineEdit().setReadOnly(True)
            spinner.lineEdit().setFocusPolicy(Qt.NoFocus)

            initial_value = round(float(quick_weight['value']), 1)
            spinner.setValue(initial_value)

            spinner.valueChanged.connect(self.save_quick_weight)

            self.spinner_grid.addWidget(spinner, row, column)

            column += 1
            if column == 2:
                column = 0
                row += 1

    def save_quick_weight(self):
        spinner = self.sender()
        if spinner is None or self.current_character_name is None:
            return

        tag = spinner.property("tag")
        negative = spinner.property("negative")

        raw_value = float(spinner.value())
        new_value = round(raw_value, 1)

        spinner.blockSignals(True)
        spinner.setValue(new_value)
        spinner.blockSignals(False)

        for entry in self.quick_weights_data:
            if entry["tag"] == tag and entry["negative"] == negative:
                entry["value"] = new_value
                break

        self.quickWeightsChanged.emit(self.current_character_name, self.quick_weights_data)
