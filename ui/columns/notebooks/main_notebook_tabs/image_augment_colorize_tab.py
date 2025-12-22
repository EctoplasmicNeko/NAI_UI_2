from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox, QTextEdit


class ImageAugmentColorizeTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_augment_colorize_tab()

    def build_image_augment_colorize_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.colorize_strength_combobox = QComboBox(self)
        self.colorize_strength_combobox.addItems(['Normal', 'Slightly Weak', 'Weak', 'Even Weaker', 'Very Weak', 'Weakest'])
        self.colorize_strength_combobox.setCurrentIndex(0)
        self.grid.addWidget(self.colorize_strength_combobox, 1, 0, 1, 2) 

        self.colorize_prompt = QTextEdit()
        self.colorize_prompt.setPlaceholderText("Insert Prompt")
        self.grid.addWidget(self.colorize_prompt, 2, 0, 1, 2)


    def export_state(self):

        colorize_strength = self.colorize_strength_combobox.currentText()
        strength_list =[('Normal', 0), ('Slightly Weak', 1), ('Weak', 2), ('Even Weaker', 3), ('Very Weak', 4), ('Weakest', 5)]
        for i in strength_list:
            if i[0] == colorize_strength:
                selected_strength = i[1]

        return {
            'colorize_strength': self.colorize_strength_combobox.currentData(),
            'colorize_strength_weight': selected_strength,
            'colorize_prompt': self.colorize_prompt.toPlainText()
        }
    
    def import_state(self, loaded):
        self.colorize_strength_combobox.setCurrentText(loaded['colorize_strength'])
        self.colorize_prompt.setText(loaded['colorize_prompt'])
        