from PySide6.QtWidgets import QGridLayout, QFrame,QPushButton, QSizePolicy, QListWidget, QComboBox, QSpinBox, QLineEdit, QCheckBox
from data.datahub import get_data, get_all_characters
from widget import decorated_combobox


class WorkflowTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_workflow_tab()
        self.hide_filters()
        self.hide_sort_by_name()
    
    def build_workflow_tab(self):
        
        self.requests = get_data("requests", [])                
        self.request_list = [f'{request["name"]}' for request in self.requests]

        self.characters = get_all_characters()

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.task_frame = QFrame(self)
        self.task_frame_grid = QGridLayout(self.task_frame)
        self.grid.addWidget(self.task_frame)

        self.task_combo = QComboBox(self.task_frame)
        self.task_combo.addItems(self.request_list)
        self.task_frame_grid.addWidget(self.task_combo, 0, 0)

        self.add_task_button = QPushButton('Add Task',self.task_frame)
        self.add_task_button.clicked.connect(lambda: self.list.addItem(self.task_combo.currentText()))
        self.task_frame_grid.addWidget(self.add_task_button, 0, 1)

        self.remove_task_button = QPushButton('Remove Task',self.task_frame)
        self.remove_task_button.clicked.connect(lambda: self.list.takeItem(self.list.currentRow()))
        self.task_frame_grid.addWidget(self.remove_task_button, 0, 2)

        self.loops = QSpinBox(self)
        self.loops.setPrefix("Loops: ")
        self.loops.setMinimum(1)
        self.task_frame_grid.addWidget(self.loops, 1, 0)

        self.sets = QSpinBox(self)
        self.sets.setPrefix("Sets: ")
        self.sets.setMinimum(0)
        self.sets.setSpecialValueText("Per Character")
        self.task_frame_grid.addWidget(self.sets, 1, 1)
        self.sets.valueChanged.connect(lambda: self.hide_filters())

        self.cancel_task_button = QPushButton('Cancel Task',self.task_frame)
        self.cancel_task_button.clicked.connect(lambda: self.cycle_list())
        self.task_frame_grid.addWidget(self.cancel_task_button, 1, 2)

        self.filter_frame = QFrame(self)
        self.filter_frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.task_frame_grid.addWidget(self.filter_frame, 2, 0, 1, 3) 
        self.filter_frame_grid = QGridLayout(self.filter_frame) 

        self.filter1_combo = decorated_combobox.DecoratedComboBox(self)
        self.filter1_combo.addItems(["None"] + list(self.load_tags()))
        self.filter1_combo.setPrefix("Filter: ")
        self.filter_frame_grid.addWidget(self.filter1_combo, 2, 0)

        self.filter2_combo = decorated_combobox.DecoratedComboBox(self)
        self.filter2_combo.addItems(["None"] + list(self.load_tags()))
        self.filter2_combo.setPrefix("Filter: ")
        self.filter_frame_grid.addWidget(self.filter2_combo, 2, 1)

        self.filter3_combo = decorated_combobox.DecoratedComboBox(self)
        self.filter3_combo.setPrefix("Filter: ")
        self.filter3_combo.addItems(["None"] + list(self.load_tags()))
        self.filter_frame_grid.addWidget(self.filter3_combo, 2, 2)

        self.sorting_frame = QFrame(self)
        self.grid.addWidget(self.sorting_frame, 4, 0)
        self.sorting_frame_grid = QGridLayout(self.sorting_frame)
        self.sorting_frame_grid.setContentsMargins(0,0,0,3)
        self.sorting_frame_grid.setSpacing(3)
        self.sorting_frame_grid.setRowStretch(0, 0)
        self.sorting_frame_grid.setRowStretch(1, 0)
        self.sorting_frame_grid.setColumnStretch(0, 1)
        self.sorting_frame_grid.setColumnStretch(1, 1)
        self.sorting_frame_grid.setColumnStretch(2, 1)


        self.sort_by_name_checkbox = QCheckBox('Sort by Name', self)
        self.sorting_frame_grid.addWidget(self.sort_by_name_checkbox, 0, 0)

        self.sort_by_character_checkbox = QCheckBox('Sort by Character', self)
        self.sorting_frame_grid.addWidget(self.sort_by_character_checkbox, 0, 1)

        self.sort_by_date_checkbox = QCheckBox('Sort by Date', self)
        self.sorting_frame_grid.addWidget(self.sort_by_date_checkbox, 0, 2)

        self.sort_by_name_lineedit = QLineEdit(self)
        self.sort_by_name_lineedit.setPlaceholderText('Set Name')
        self.sorting_frame_grid.addWidget(self.sort_by_name_lineedit, 1, 0)

        self.sort_by_name_checkbox.stateChanged.connect(lambda: self.hide_sort_by_name())

        self.list = QListWidget(self)
        self.grid.addWidget(self.list, 5, 0)


    def hide_sort_by_name(self):
        if self.sort_by_name_checkbox.isChecked():
            self.sort_by_name_lineedit.show()
        else:
            self.sort_by_name_lineedit.hide() 

    def load_tags(self):
        tag_list = []
        for character in self.characters:
            for tag in character.get("tags", []):
                if tag not in tag_list:
                    tag_list.append(tag)
            
        return tag_list
    
    def determine_list_length(self):
        length = 0
        for character in self.characters:
            if self.filter1_combo.currentText() in character.get("tags", []) or self.filter1_combo.currentText() == "None":
                if self.filter2_combo.currentText() in character.get("tags", []) or self.filter2_combo.currentText() == "None":
                    if self.filter3_combo.currentText() in character.get("tags", []) or self.filter3_combo.currentText() == "None":
                        length += 1
        return length
                        


    def cycle_list(self):
        list_length = self.list.count()
        item = self.list.takeItem(0)
        self.list.insertItem(list_length, item)
    
    def export_state(self):
        item = self.list.item(0) #this part gets the current next task for generation
        current_request = item.text()
        for request in self.requests:
            if current_request == request['name']:
                request_name = request['request_name']
                request_url = request['request_url']
                
        return {
          'request_name':request_name,
          'request_url': request_url,
          "task_list": [
            self.list.item(i).text()
            for i in range(self.list.count())
        ],
        'loops': self.loops.value(),
        'sets': self.sets.value(),
        'filter_1': self.filter1_combo.currentText(),
        'filter_2': self.filter2_combo.currentText(),
        'filter_3': self.filter3_combo.currentText(),
        'organize_outputs_by_name': self.sort_by_name_checkbox.isChecked(),
        'organize_outputs_by_character': self.sort_by_character_checkbox.isChecked(),
        'organize_outputs_by_date': self.sort_by_date_checkbox.isChecked(),
        'folder_name': self.sort_by_name_lineedit.text()    
        }

    def import_state(self, loaded):
        self.list.clear()
        self.list.addItems(loaded['task_list'])
        self.loops.setValue(loaded.get('loops', 1))
        self.sets.setValue(loaded.get('sets', 0))
        self.filter1_combo.setCurrentText(loaded.get('filter_1', 'None'))
        self.filter2_combo.setCurrentText(loaded.get('filter_2', 'None'))
        self.filter3_combo.setCurrentText(loaded.get('filter_3', 'None'))

    def hide_filters(self):
        if self.sets.value() != 0:
          self.filter_frame.hide()
        else:
          self.filter_frame.show()