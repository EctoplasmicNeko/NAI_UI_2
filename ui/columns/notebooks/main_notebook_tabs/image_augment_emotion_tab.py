from PySide6.QtWidgets import QGridLayout, QFrame, QComboBox, QTextEdit

class ImageAugmentEmotionTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_augment_emotion_tab()

    def build_image_augment_emotion_tab(self):

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.emotion_comboxbox = QComboBox(self)
        self.emotion_comboxbox.addItems(['Angry','Aroused','Bored','Confused','Determined','Disgusted','Embarrassed','Excited','Happy','Hurt','Irritated','Laughing','Love','Nervous','Neutral','Playful','Sad','Scared','Shy','Smug','Surprised','Thinking','Tired','Worried'])
        self.emotion_comboxbox.setCurrentIndex(1)
        self.grid.addWidget(self.emotion_comboxbox, 1, 0, 1, 2) 

        self.emotion_strength_combobox = QComboBox(self)
        self.emotion_strength_combobox.addItems(['Normal', 'Slightly Weak', 'Weak', 'Even Weaker', 'Very Weak', 'Weakest'])
        self.emotion_strength_combobox.setCurrentIndex(0)
        self.grid.addWidget(self.emotion_strength_combobox, 2, 0, 1, 2) 

        self.emotion_prompt = QTextEdit()
        self.emotion_prompt.setPlaceholderText("Insert Prompt")
        self.grid.addWidget(self.emotion_prompt, 3, 0, 1, 2)

    def export_state(self):
        
        emotion_strength = self.emotion_strength_combobox.currentText()
        strength_list =[('Normal', 0), ('Slightly Weak', 1), ('Weak', 2), ('Even Weaker', 3), ('Very Weak', 4), ('Weakest', 5)]
        for i in strength_list:
            if i[0] == emotion_strength:
                selected_strength = i[1]
        
        emotion_type = self.emotion_comboxbox.currentText()
        emotion_prompt = self.emotion_prompt.toPlainText()
        
        return {
            'emotion_type': emotion_type,
            'emotion_strength': emotion_strength,
            'emotion_prompt': emotion_prompt,
            'emotion_strength_weight': selected_strength, #used by generate
            'emotion_merged_prompt': (f'{emotion_type.lower()};;{emotion_prompt}')
        }
    
    def import_state(self, loaded):
        self.emotion_comboxbox.setCurrentText(loaded['emotion_type'])
        self.emotion_strength_combobox.setCurrentText(loaded['emotion_strength'])
        self.emotion_prompt.setText(loaded['emotion_prompt'])

