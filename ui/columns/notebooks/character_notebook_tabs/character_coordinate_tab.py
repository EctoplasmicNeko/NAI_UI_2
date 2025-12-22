from PySide6.QtWidgets import QGridLayout, QFrame,QPushButton, QSizePolicy, QButtonGroup



class CharacterCoordinateTab(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_character_coordinate_tab()

    def build_character_coordinate_tab(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.coordinate_frame = QFrame(self)
        self.coordinate_frame_grid = QGridLayout(self.coordinate_frame)
        self.coordinate_frame.setStyleSheet("""
                    QPushButton {
                        padding: 2px 4px;
                        margin: 0px;
                        border: 1px solid #aaa;
                        border-radius: 2px;
                    }
                    QPushButton:checked {
                        background-color: #336699;
                        color: white;
                    }
                """)
        self.grid.addWidget(self.coordinate_frame)

        self.coordinate_button_group = QButtonGroup(self.coordinate_frame)
        self.coordinate_button_group.setExclusive(True)

        horizontal = [('A', 0.1), ('B', 0.3), ('C', 0.5), ('D', 0.7), ('E', 0.9)]
        vertical = [('1', 0.1), ('2', 0.3), ('3', 0.5), ('4', 0.7), ('5', 0.9)]

        id = 1
        for v_index, (v_label, v_coord) in enumerate(vertical):
            for h_index, (h_label, h_coord) in enumerate(horizontal):
                btn = QPushButton(f'{h_label}{v_label}', self.coordinate_frame)
                btn.setCheckable(True)
                btn.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
                btn.setMinimumSize(24, 24)
                btn.setProperty("coordinates", (h_coord, v_coord))
                
                self.coordinate_frame_grid.addWidget(btn, v_index, h_index)
                self.coordinate_button_group.addButton(btn, id)
                id += 1

        self.coordinate_none_button = QPushButton('None', self.coordinate_frame)
        self.coordinate_none_button.setCheckable(True)
        self.coordinate_none_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
        self.coordinate_none_button.setMinimumSize(24, 24)
        self.coordinate_none_button.setProperty("coordinates", (0, 0))
        self.coordinate_frame_grid.addWidget(self.coordinate_none_button, len(vertical), 0, 1, len(horizontal))
        self.coordinate_button_group.addButton(self.coordinate_none_button, 0)
                



            
