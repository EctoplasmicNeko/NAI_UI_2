from PySide6.QtWidgets import QGridLayout, QFrame, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox, QLabel, QProgressBar, QSizePolicy
from PySide6.QtCore import Qt
from data.datahub import get_data
from widget.Qseedbox import SeedSpinBox


class ImageGenerateSettingsTab(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_generate_settings_tab()
        self.setObjectName("image_generate_settings_tab")
        
    def build_image_generate_settings_tab(self):

        #gather data
        self.models = get_data("models") #load the models dictionary from the data cache
        self.model_names = [model["name"] for model in self.models.values()]

        self.samplers = get_data("samplers") #load the models dictionary from the data cache
        self.sampler_names = [sampler["name"] for sampler in self.samplers.values()]

        self.schedules = get_data("schedules") #load the models dictionary from the data cache
        self.schedule_names = [schedule["name"] for schedule in self.schedules.values()]

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 5, 0, 5)
        self.grid.setSpacing(3)
        self.grid.setColumnStretch(0,45)
        self.grid.setColumnStretch(1,45) 
        self.grid.setColumnStretch(2,10)

        self.generate_progress_bar_frame = QFrame(self)
        self.generate_progress_bar_frame.setObjectName("generate_progress_bar_frame")
        self.generate_progress_bar_frame_grid = QGridLayout(self.generate_progress_bar_frame)
        self.generate_progress_bar_frame.setFrameShape(QFrame.StyledPanel)
        self.generate_progress_bar_frame.setFrameShadow(QFrame.Raised)
        self.grid.addWidget(self.generate_progress_bar_frame, 0, 2, 5, 1)
        
        self.generate_progress_bar_frame_grid.setContentsMargins(0, 0, 0, 0)
        self.generate_progress_bar_frame_grid.setSpacing(0)
        self.generate_progress_bar_frame_grid.setColumnStretch(0, 1)
        self.generate_progress_bar_frame_grid.setColumnStretch(1, 1)
        self.generate_progress_bar_frame_grid.setRowStretch(0, 1)
        self.generate_progress_bar_frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.generate_progress_set_bar = QProgressBar(self.generate_progress_bar_frame)
        self.generate_progress_set_bar.setObjectName("generate_progress_set_bar")
        self.generate_progress_set_bar.setOrientation(Qt.Vertical)
        self.generate_progress_set_bar.setRange(0, 1)
        self.generate_progress_set_bar.setValue(0)
        self.generate_progress_set_bar.setTextVisible(False)
        self.generate_progress_set_bar.setAlignment(Qt.AlignCenter)
        self.generate_progress_set_bar.setObjectName("generate_progress_set_bar")
        self.generate_progress_set_bar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.generate_progress_bar_frame_grid.addWidget(self.generate_progress_set_bar, 0, 0)

        self.generate_progress_loop_bar = QProgressBar(self.generate_progress_bar_frame)
        self.generate_progress_loop_bar.setObjectName("generate_progress_loop_bar")
        self.generate_progress_loop_bar.setOrientation(Qt.Vertical)
        self.generate_progress_loop_bar.setRange(0, 1)
        self.generate_progress_loop_bar.setValue(0)
        self.generate_progress_loop_bar.setTextVisible(False)
        self.generate_progress_loop_bar.setAlignment(Qt.AlignCenter)
        self.generate_progress_loop_bar.setObjectName("generate_progress_loop_bar")
        self.generate_progress_loop_bar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.generate_progress_bar_frame_grid.addWidget(self.generate_progress_loop_bar, 0, 1)


        # ---- model (str)
        self.model_select_combobox = QComboBox(self)
        self.model_select_combobox.setObjectName("model_select_combobox")
        self.model_select_combobox.addItems(self.model_names)
        self.grid.addWidget(self.model_select_combobox, 0, 0)

        self.model_select_label = QLabel("Model")
        self.model_select_label.setObjectName("model_select_label")
        self.grid.addWidget(self.model_select_label, 0, 1)

        # ---- sampler (str)
        self.sampler_select_combobox = QComboBox(self)
        self.sampler_select_combobox.setObjectName("sampler_select_combobox")
        self.sampler_select_combobox.currentIndexChanged.connect(self.update_sampler_properties)
        self.grid.addWidget(self.sampler_select_combobox, 1, 0)

        self.sampler_select_label = QLabel("Sampler")
        self.sampler_select_label.setObjectName("sampler_select_label")
        self.grid.addWidget(self.sampler_select_label, 1, 1)

        # ---- schedule (str)
        self.schedule_select_combobox = QComboBox(self)
        self.schedule_select_combobox.setObjectName("schedule_select_combobox")
        self.schedule_select_combobox.currentIndexChanged.connect(self.update_schedule_properties)
        self.grid.addWidget(self.schedule_select_combobox, 2, 0)

        self.schedule_select_label = QLabel("Schedule")
        self.schedule_select_label.setObjectName("schedule_select_label")
        self.grid.addWidget(self.schedule_select_label, 2, 1)

        # - N Images parameter was here but I deleted it since realistically it's never necessary with the automated loops, and really nobody with Opus would ever need it.

        # ---- steps (int)
        self.steps_select_counter = QSpinBox(self)
        self.steps_select_counter.setObjectName("steps_select_counter")
        self.steps_select_counter.setRange(1, 50)
        self.steps_select_counter.setSingleStep(1)
        self.steps_select_counter.valueChanged.connect(self.costs_anlas)
        self.grid.addWidget(self.steps_select_counter, 3, 0)
        

        self.steps_select_label = QLabel("Steps")
        self.steps_select_label.setObjectName("steps_select_label")
        self.grid.addWidget(self.steps_select_label, 3, 1)

        # ---- scale (float)
        self.scale_select_counter = QDoubleSpinBox(self) 
        self.scale_select_counter.setObjectName("scale_select_counter")
        self.scale_select_counter.setRange(1.0, 10.0) 
        self.scale_select_counter.setSingleStep(0.1) 
        self.scale_select_counter.setDecimals(1)
        self.grid.addWidget(self.scale_select_counter, 4, 0)

        self.scale_select_label = QLabel("Scale")
        self.scale_select_label.setObjectName("scale_select_label")
        self.grid.addWidget(self.scale_select_label, 4, 1)

        # ---- rescale (float)
        self.rescale_select_counter = QDoubleSpinBox(self)
        self.rescale_select_counter.setObjectName("rescale_select_counter")
        self.rescale_select_counter.setRange(0.0, 1.0) 
        self.rescale_select_counter.setSingleStep(0.02) 
        self.rescale_select_counter.setDecimals(2)
        self.rescale_select_counter.setSpecialValueText("Disabled") 

        self.grid.addWidget(self.rescale_select_counter, 5, 0)

        self.rescale_select_label = QLabel("Rescale")
        self.rescale_select_label.setObjectName("rescale_select_label")
        self.grid.addWidget(self.rescale_select_label, 5, 1)

        self.rescale_disable_button = QPushButton("Ø", self)
        self.rescale_disable_button.setObjectName("rescale_disable_button")
        self.rescale_disable_button.clicked.connect(lambda: self.rescale_select_counter.setValue(0.0))
        self.rescale_disable_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.grid.addWidget(self.rescale_disable_button, 5, 2)

        # ---- cfg (int; allows -1)
        self.cfg_select_counter = QSpinBox(self) 
        self.cfg_select_counter.setObjectName("cfg_select_counter")
        self.cfg_select_counter.setMinimum(-1)
        self.cfg_select_counter.setSingleStep(1)
        self.cfg_select_counter.setSpecialValueText("Disabled") 
        self.grid.addWidget(self.cfg_select_counter, 6, 0)

        self.cfg_select_label = QLabel("CFG")
        self.cfg_select_label.setObjectName("cfg_select_label")
        self.grid.addWidget(self.cfg_select_label, 6, 1)

        self.cfg_disable_button = QPushButton("Ø", self)
        self.cfg_disable_button.setObjectName("cfg_disable_button")
        self.cfg_disable_button.clicked.connect(lambda: self.cfg_select_counter.setValue(-1))
        self.cfg_disable_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.grid.addWidget(self.cfg_disable_button, 6, 2)

               # ---- seed(int)
        self.seed_select_counter = SeedSpinBox(self) 
        self.seed_select_counter.setObjectName("seed_select_counter")
        self.seed_select_counter.setRange(0, 4294967294); 
        self.seed_select_counter.setSingleStep(1)
        self.seed_select_counter.setSpecialValueText("Random") 
        self.grid.addWidget(self.seed_select_counter, 7, 0)

        self.seed_select_label = QLabel("Seed")
        self.seed_select_label.setObjectName("seed_select_label")
        self.grid.addWidget(self.seed_select_label, 7, 1)

        self.seed_zero_button = QPushButton("Ø", self)
        self.seed_zero_button.setObjectName("seed_zero_button")
        self.seed_zero_button.clicked.connect(lambda: self.seed_select_counter.setValue(0))
        self.seed_zero_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        self.grid.addWidget(self.seed_zero_button, 7, 2)

    def update_sampler_properties(self):
        current_sampler = self.sampler_select_combobox.currentText()
        for sampler in self.samplers.values():
            if current_sampler == sampler["name"]:
                self.sampler_select_combobox.setProperty("sampler", sampler['payload_name'])

    def update_schedule_properties(self):
        current_schedule = self.schedule_select_combobox.currentText()
        for schedule in self.schedules.values():
            if current_schedule == schedule["name"]:
                self.schedule_select_combobox.setProperty("schedule", schedule['payload_name'])

    def costs_anlas(self):
        current_steps = self.steps_select_counter.value()
        if current_steps > 28:
            self.steps_select_counter.setStyleSheet("background: #E57373")
        else:
            self.steps_select_counter.setStyleSheet("") 
  
        