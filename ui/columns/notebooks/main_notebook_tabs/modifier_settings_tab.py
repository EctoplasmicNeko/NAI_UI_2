from PySide6.QtWidgets import QGridLayout, QFrame, QScrollArea, QVBoxLayout, QSizePolicy, QSpinBox, QCheckBox, QSpacerItem, QDoubleSpinBox
from PySide6.QtCore import Qt

class ModifierSettingsTab(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_modifier_settings_tab()
        self.modifiers_ui_init()

    def build_modifier_settings_tab(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # 1) Make one scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)                          # critical: width follows viewport
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setAlignment(Qt.AlignTop)
        self.grid.addWidget(self.scroll, 0, 0)

        # 2) Real content lives in here
        self.inner = QFrame()
        self.inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.inner_grid = QGridLayout(self.inner)
        self.inner_grid.setContentsMargins(0, 0, 0, 0)
        self.inner_grid.setSpacing(3)
        self.inner_grid.setColumnStretch(0, 1)
        self.inner_grid.setColumnStretch(1, 1)
        self.inner_grid.setColumnStretch(2, 1)

        self.grid.setRowStretch(0, 0)   
        self.grid.setRowStretch(1, 0)   
        self.grid.setRowStretch(2, 0)   
        self.grid.setRowStretch(3, 0)   
        self.grid.setRowStretch(4, 0)   
        self.grid.setRowStretch(5, 0)   
        self.grid.setRowStretch(6, 0)   
        self.grid.setRowStretch(7, 0)   
        self.grid.setRowStretch(8, 0)   
        self.grid.setRowStretch(9, 0)   
        self.grid.setRowStretch(10, 0)   
        self.grid.setRowStretch(11, 1)   

        self.scroll.setWidget(self.inner)

        # --- sampler Creep ---

        self.sampler_creep_checkbox = QCheckBox("Sampler Creep", self.inner)
        self.sampler_creep_checkbox.toggled.connect(self.adjust_sampler_creep_ui)
        self.inner_grid.addWidget(self.sampler_creep_checkbox, 0, 0)

        self.sampler_creep_frequency_counter = QSpinBox(self.inner)
        self.sampler_creep_frequency_counter.setSingleStep(1)
        self.sampler_creep_frequency_counter.setPrefix("Frequency:   ")
        self.sampler_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.sampler_creep_frequency_counter, 0, 1)

        # --- Schedule Creep ---

        self.schedule_creep_checkbox = QCheckBox("Schedule Creep", self.inner)
        self.schedule_creep_checkbox.toggled.connect(self.adjust_schedule_creep_ui)
        self.inner_grid.addWidget(self.schedule_creep_checkbox, 1, 0)

        self.schedule_creep_frequency_counter = QSpinBox(self.inner)
        self.schedule_creep_frequency_counter.setSingleStep(1)
        self.schedule_creep_frequency_counter.setPrefix("Frequency:   ")
        self.schedule_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.schedule_creep_frequency_counter, 1, 1)

        # --- Seed Creep ---

        self.seed_creep_checkbox = QCheckBox("Seed Creep", self.inner)
        self.seed_creep_checkbox.toggled.connect(self.adjust_seed_creep_ui)
        self.inner_grid.addWidget(self.seed_creep_checkbox, 2, 0)

        self.seed_creep_frequency_counter = QSpinBox(self.inner)
        self.seed_creep_frequency_counter.setSingleStep(1)
        self.seed_creep_frequency_counter.setPrefix("Frequency:   ")
        self.seed_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.seed_creep_frequency_counter, 2, 1)

        self.seed_creep_increment_counter = QSpinBox(self.inner)
        self.seed_creep_increment_counter.setSingleStep(1)
        self.seed_creep_increment_counter.setPrefix("Increment:   ")
        self.seed_creep_increment_counter.setMinimum(0)
        self.inner_grid.addWidget(self.seed_creep_increment_counter, 2, 2)

        # --- Steps Creep ---

        self.steps_creep_checkbox = QCheckBox("Steps Creep", self.inner)
        self.steps_creep_checkbox.toggled.connect(self.adjust_steps_creep_ui)
        self.inner_grid.addWidget(self.steps_creep_checkbox, 3, 0)

        self.steps_creep_frequency_counter = QSpinBox(self.inner)
        self.steps_creep_frequency_counter.setSingleStep(1)
        self.steps_creep_frequency_counter.setPrefix("Frequency:   ")
        self.steps_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.steps_creep_frequency_counter, 3, 1)

        self.steps_creep_increment_counter = QSpinBox(self.inner)
        self.steps_creep_increment_counter.setSingleStep(1)
        self.steps_creep_increment_counter.setPrefix("Increment:   ")
        self.steps_creep_increment_counter.setMinimum(0)
        self.inner_grid.addWidget(self.steps_creep_increment_counter, 3, 2)

        self.steps_creep_min_counter = QSpinBox(self.inner)
        self.steps_creep_min_counter.setSingleStep(1)
        self.steps_creep_min_counter.setPrefix("Min:   ")
        self.steps_creep_min_counter.setMinimum(0)
        self.inner_grid.addWidget(self.steps_creep_min_counter, 4, 1)

        self.steps_creep_max_counter = QSpinBox(self.inner)
        self.steps_creep_max_counter.setSingleStep(1)
        self.steps_creep_max_counter.setPrefix("Max:   ")
        self.steps_creep_max_counter.setMinimum(0)
        self.inner_grid.addWidget(self.steps_creep_max_counter, 4, 2)

        # --- Scale Creep ---

        self.scale_creep_checkbox = QCheckBox("Scale Creep", self.inner)
        self.scale_creep_checkbox.toggled.connect(self.adjust_scale_creep_ui)
        self.inner_grid.addWidget(self.scale_creep_checkbox, 5, 0)

        self.scale_creep_frequency_counter = QSpinBox(self.inner)
        self.scale_creep_frequency_counter.setSingleStep(1)
        self.scale_creep_frequency_counter.setPrefix("Frequency:   ")
        self.scale_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.scale_creep_frequency_counter, 5, 1)

        self.scale_creep_increment_counter = QDoubleSpinBox(self.inner)
        self.scale_creep_increment_counter.setSingleStep(0.1)
        self.scale_creep_increment_counter.setPrefix("Increment:   ")
        self.scale_creep_increment_counter.setDecimals(1)
        self.scale_creep_increment_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.scale_creep_increment_counter, 5, 2)

        self.scale_creep_min_counter = QDoubleSpinBox(self.inner)
        self.scale_creep_min_counter.setSingleStep(0.1)
        self.scale_creep_min_counter.setPrefix("Min:   ")
        self.scale_creep_min_counter.setDecimals(1)
        self.scale_creep_min_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.scale_creep_min_counter, 6, 1)

        self.scale_creep_max_counter = QDoubleSpinBox(self.inner)
        self.scale_creep_max_counter.setSingleStep(0.1)
        self.scale_creep_max_counter.setPrefix("Max:   ")
        self.scale_creep_max_counter.setDecimals(1)
        self.scale_creep_max_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.scale_creep_max_counter, 6, 2)

        # --- CFG Creep ---

        self.cfg_creep_checkbox = QCheckBox("CFG Creep", self.inner)
        self.cfg_creep_checkbox.toggled.connect(self.adjust_cfg_creep_ui)
        self.inner_grid.addWidget(self.cfg_creep_checkbox, 7, 0)

        self.cfg_creep_frequency_counter = QSpinBox(self.inner)
        self.cfg_creep_frequency_counter.setSingleStep(1)
        self.cfg_creep_frequency_counter.setPrefix("Frequency:   ")
        self.cfg_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.cfg_creep_frequency_counter, 7, 1)

        self.cfg_creep_increment_counter = QDoubleSpinBox(self.inner)
        self.cfg_creep_increment_counter.setSingleStep(0.1)
        self.cfg_creep_increment_counter.setPrefix("Increment:   ")
        self.cfg_creep_increment_counter.setDecimals(1)
        self.cfg_creep_increment_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.cfg_creep_increment_counter, 7, 2)

        self.cfg_creep_min_counter = QDoubleSpinBox(self.inner)
        self.cfg_creep_min_counter.setSingleStep(0.1)
        self.cfg_creep_min_counter.setPrefix("Min:   ")
        self.cfg_creep_min_counter.setDecimals(1)
        self.cfg_creep_min_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.cfg_creep_min_counter, 8, 1)

        self.cfg_creep_max_counter = QDoubleSpinBox(self.inner)
        self.cfg_creep_max_counter.setSingleStep(0.1)
        self.cfg_creep_max_counter.setPrefix("Max:   ")
        self.cfg_creep_max_counter.setDecimals(1)
        self.cfg_creep_max_counter.setMinimum(0.0)
        self.inner_grid.addWidget(self.cfg_creep_max_counter, 8, 2)

        # --- Artist Creep ---

        self.artist_creep_checkbox = QCheckBox("Artist Creep", self.inner)
        self.artist_creep_checkbox.toggled.connect(self.adjust_artist_creep_ui)
        self.inner_grid.addWidget(self.artist_creep_checkbox, 9, 0)

        self.artist_creep_frequency_counter = QSpinBox(self.inner)
        self.artist_creep_frequency_counter.setSingleStep(1)
        self.artist_creep_frequency_counter.setPrefix("Frequency:   ")
        self.artist_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.artist_creep_frequency_counter, 9, 1)

        # --- Vibe Creep ---

        self.vibe_creep_checkbox = QCheckBox("Vibe Creep", self.inner)
        self.vibe_creep_checkbox.toggled.connect(self.adjust_vibe_creep_ui)
        self.inner_grid.addWidget(self.vibe_creep_checkbox, 10, 0)

        self.vibe_creep_frequency_counter = QSpinBox(self.inner)
        self.vibe_creep_frequency_counter.setSingleStep(1)
        self.vibe_creep_frequency_counter.setPrefix("Frequency:   ")
        self.vibe_creep_frequency_counter.setMinimum(0)
        self.inner_grid.addWidget(self.vibe_creep_frequency_counter, 10, 1)

    def adjust_sampler_creep_ui(self):
        state = self.sampler_creep_checkbox.isChecked()
        if state:
                self.sampler_creep_frequency_counter.setDisabled(False)
        else:
            self.sampler_creep_frequency_counter.setDisabled(True)
            
    def adjust_schedule_creep_ui(self):
        state = self.schedule_creep_checkbox.isChecked()
        if state:
                self.schedule_creep_frequency_counter.setDisabled(False)
        else:
            self.schedule_creep_frequency_counter.setDisabled(True)

    def adjust_seed_creep_ui(self):
        state = self.seed_creep_checkbox.isChecked()
        if state:
                self.seed_creep_frequency_counter.setDisabled(False)
                self.seed_creep_increment_counter.setDisabled(False)
        else:
            self.seed_creep_frequency_counter.setDisabled(True)
            self.seed_creep_increment_counter.setDisabled(True)

    def adjust_steps_creep_ui(self):
        state = self.steps_creep_checkbox.isChecked()
        if state:
                self.steps_creep_frequency_counter.setDisabled(False)
                self.steps_creep_increment_counter.setDisabled(False)
                self.steps_creep_min_counter.setDisabled(False)
                self.steps_creep_max_counter.setDisabled(False)

        else:
            self.steps_creep_frequency_counter.setDisabled(True)
            self.steps_creep_increment_counter.setDisabled(True)
            self.steps_creep_min_counter.setDisabled(True)
            self.steps_creep_max_counter.setDisabled(True)

    def adjust_scale_creep_ui(self):
        state = self.scale_creep_checkbox.isChecked()
        if state:
                self.scale_creep_frequency_counter.setDisabled(False)
                self.scale_creep_increment_counter.setDisabled(False)
                self.scale_creep_min_counter.setDisabled(False)
                self.scale_creep_max_counter.setDisabled(False)

        else:
            self.scale_creep_frequency_counter.setDisabled(True)
            self.scale_creep_increment_counter.setDisabled(True)
            self.scale_creep_min_counter.setDisabled(True)
            self.scale_creep_max_counter.setDisabled(True)

    def adjust_cfg_creep_ui(self):
        state = self.cfg_creep_checkbox.isChecked()
        if state:
                self.cfg_creep_frequency_counter.setDisabled(False)
                self.cfg_creep_increment_counter.setDisabled(False)
                self.cfg_creep_min_counter.setDisabled(False)
                self.cfg_creep_max_counter.setDisabled(False)

        else:
            self.cfg_creep_frequency_counter.setDisabled(True)
            self.cfg_creep_increment_counter.setDisabled(True)
            self.cfg_creep_min_counter.setDisabled(True)
            self.cfg_creep_max_counter.setDisabled(True)

    def adjust_artist_creep_ui(self):
        state = self.artist_creep_checkbox.isChecked()
        if state:
                self.artist_creep_frequency_counter.setDisabled(False)

        else:
            self.artist_creep_frequency_counter.setDisabled(True)

    def adjust_vibe_creep_ui(self):
        state = self.vibe_creep_checkbox.isChecked()
        if state:
                self.vibe_creep_frequency_counter.setDisabled(False)

        else:
            self.vibe_creep_frequency_counter.setDisabled(True)

    def modifiers_ui_init(self):
         self.adjust_sampler_creep_ui()
         self.adjust_schedule_creep_ui()
         self.adjust_seed_creep_ui()
         self.adjust_steps_creep_ui()
         self.adjust_scale_creep_ui()
         self.adjust_cfg_creep_ui()
         self.adjust_artist_creep_ui()
         self.adjust_vibe_creep_ui()


"""
this whole tab is basically bad code, there are much better ways to build the tab and to run functions in it. Also, consider putting all the sections in their 
own container and using 3columns of stretch,. It's fine as it is but that would give more flexibility for coloring it in.  
"""

         






        

        

        

        

        

        

        

        

        
