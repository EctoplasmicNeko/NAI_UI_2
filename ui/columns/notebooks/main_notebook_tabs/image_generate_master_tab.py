from PySide6.QtWidgets import QGridLayout, QFrame

from ui.columns.notebooks.main_notebook_tabs.image_generate_settings_tab import ImageGenerateSettingsTab
from ui.columns.notebooks.main_notebook_tabs.image_generate_buttons_tab import ImageGenerateButtonsTab
from ui.columns.notebooks.main_notebook_tabs.image_generate_sizes_tab import ImageGenerateSizesTab


class ImageGenerateMasterTab(QFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self.build_image_generate_master_tab()
        self.refresh_UI_by_model()

    def build_image_generate_master_tab(self):    

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(5)

        self.image_settings_tab = ImageGenerateSettingsTab(self)
        self.grid.addWidget(self.image_settings_tab, 0, 0)

        self.image_buttons_tab = ImageGenerateButtonsTab(self)
        self.grid.addWidget(self.image_buttons_tab, 1, 0)

        self.image_sizes_tab = ImageGenerateSizesTab(self)
        self.grid.addWidget(self.image_sizes_tab, 2, 0)

        self.grid.setRowStretch(3, 1) 

        self.image_settings_tab.model_select_combobox.currentIndexChanged.connect(self.refresh_UI_by_model)        
    
    def export_state(self):

        scale = self.image_settings_tab.scale_select_counter.value()
        scale = f"{scale:.1f}"
        scale = float(scale)

        rescale = self.image_settings_tab.rescale_select_counter.value()
        rescale = f"{rescale:.2f}"
        rescale = float(rescale)

        cfg = self.image_settings_tab.cfg_select_counter.value()
        cfg = f"{cfg:.1f}"
        cfg = float(cfg)
        

        height = int(self.image_sizes_tab.sizes_comboxbox.property('image_height'))
        width = int(self.image_sizes_tab.sizes_comboxbox.property('image_width'))

        return{
            'model': self.image_settings_tab.model_select_combobox.property('model'),
            'model_name': self.image_settings_tab.model_select_combobox.currentText(), #used by restore
            'variety+_value': self.image_settings_tab.model_select_combobox.property('variety+_value'),
            'payload_name': self.image_settings_tab.model_select_combobox.property('payload_name'),
            'payload_type': self.image_settings_tab.model_select_combobox.property('payload_type'),
            'sampler_name': self.image_settings_tab.sampler_select_combobox.currentText(),
            'sampler': self.image_settings_tab.sampler_select_combobox.property('sampler'),
            'schedule_name': self.image_settings_tab.schedule_select_combobox.currentText(),
            'schedule': self.image_settings_tab.schedule_select_combobox.property('schedule'),
            'steps': self.image_settings_tab.steps_select_counter.value(),
            'seed':  self.image_settings_tab.seed_select_counter.value(),
            'scale': scale,
            'rescale': rescale,
            'cfg':cfg,
            'legacy_v3': self.image_buttons_tab.legacy_v3_checkbox.isChecked(),
            'legacy_v4': self.image_buttons_tab.legacy_v4_checkbox.isChecked(),
            'SMEA': self.image_buttons_tab.SMEA_checkbox.isChecked(),
            'DYN': self.image_buttons_tab.DYN_checkbox.isChecked(),
            'variety+': self.image_buttons_tab.variety_checkbox.isChecked(),
            'decrisp': self.image_buttons_tab.decrisp_checkbox.isChecked(),
            'brownian': self.image_buttons_tab.brownian_checkbox.isChecked(),
            'size_name': self.image_sizes_tab.sizes_comboxbox.currentText(), #used by restore
            'image_height':height,
            'image_width': width
            }
    def import_state(self, loaded):
        self.image_settings_tab.model_select_combobox.setCurrentText(loaded['model_name'])
        self.image_settings_tab.sampler_select_combobox.setCurrentText(loaded['sampler_name'])
        self.image_settings_tab.schedule_select_combobox.setCurrentText(loaded['schedule_name'])
        self.image_settings_tab.steps_select_counter.setValue(loaded['steps'])
        self.image_settings_tab.seed_select_counter.setValue(loaded['seed'])
        self.image_settings_tab.scale_select_counter.setValue(loaded['scale'])
        self.image_settings_tab.rescale_select_counter.setValue(loaded['rescale'])
        self.image_settings_tab.cfg_select_counter.setValue(loaded['cfg'])
        self.image_buttons_tab.legacy_v3_checkbox.setChecked(loaded['legacy_v3'])
        self.image_buttons_tab.legacy_v4_checkbox.setChecked(loaded['legacy_v4'])
        self.image_buttons_tab.SMEA_checkbox.setChecked(loaded['SMEA'])
        self.image_buttons_tab.DYN_checkbox.setChecked(loaded['DYN'])
        self.image_buttons_tab.variety_checkbox.setChecked(loaded['variety+'])
        self.image_buttons_tab.decrisp_checkbox.setChecked(loaded['decrisp'])
        self.image_buttons_tab.brownian_checkbox.setChecked(loaded['brownian'])

        print(loaded['size_name'])
        print(self.image_sizes_tab.size_list)

        if loaded['size_name'] not in self.image_sizes_tab.size_list:

            match = False
            match_name = ''
            for image_size in self.image_sizes_tab.sizes:
                if int(image_size['image_height']) == loaded['image_height'] and int(image_size['image_width']) == loaded['image_width']:
                    match_name = f"{image_size['name']} {image_size['image_height']} x {image_size['image_width']}"
                    match = True
                    break
            if match:
                self.image_sizes_tab.sizes_comboxbox.setCurrentText(match_name)
                return
            else:
                self.image_sizes_tab.heights_list[0] = loaded['image_height']
                self.image_sizes_tab.width_list[0] = loaded['image_width']  
                self.image_sizes_tab.sizes_comboxbox.setItemText(0, f'Custom Size {loaded["image_height"]} x {loaded["image_width"]}')
                self.image_sizes_tab.sizes_comboxbox.setProperty('image_height', loaded['image_height'])
                self.image_sizes_tab.sizes_comboxbox.setProperty('image_width', loaded['image_width'])
                self.image_sizes_tab.sizes_comboxbox.setCurrentIndex(0)
        else:
            self.image_sizes_tab.sizes_comboxbox.setCurrentText(loaded['size_name'])


    def refresh_UI_by_model(self):
        model_name = self.image_settings_tab.model_select_combobox.currentText()
        for model in self.image_settings_tab.models.values():
            if model["name"] == model_name:
                self.image_settings_tab.model_select_combobox.setProperty('model', model["payload_name"])
                self.image_settings_tab.model_select_combobox.setProperty('variety+_value', model["model_variety+_value"])
                self.image_settings_tab.model_select_combobox.setProperty('payload_name', model["payload_name"])
                self.image_settings_tab.model_select_combobox.setProperty('payload_type', model["payload_type"])

                if model["allow_legacy_v3"]:
                    self.image_buttons_tab.legacy_v3_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.legacy_v3_checkbox.setChecked(False)
                    self.image_buttons_tab.legacy_v3_checkbox.setEnabled(False)

                if model["allow_legacy_v4"]:
                    self.image_buttons_tab.legacy_v4_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.legacy_v4_checkbox.setChecked(False)
                    self.image_buttons_tab.legacy_v4_checkbox.setEnabled(False)

                if model["allow_SMEA"]:
                    self.image_buttons_tab.SMEA_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.SMEA_checkbox.setChecked(False)
                    self.image_buttons_tab.SMEA_checkbox.setEnabled(False)

                if model["allow_SMEA"]:
                    self.image_buttons_tab.DYN_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.DYN_checkbox.setChecked(False)
                    self.image_buttons_tab.DYN_checkbox.setEnabled(False)

                if model["allow_decrisp"]:
                    self.image_buttons_tab.decrisp_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.decrisp_checkbox.setChecked(False)
                    self.image_buttons_tab.decrisp_checkbox.setEnabled(False)

                if model["allow_brownian"]:
                    self.image_buttons_tab.brownian_checkbox.setEnabled(True)
                else:
                    self.image_buttons_tab.brownian_checkbox.setChecked(False)
                    self.image_buttons_tab.brownian_checkbox.setEnabled(False)

        samplers = []
        stored_sampler = self.image_settings_tab.sampler_select_combobox.currentText()
        self.image_settings_tab.sampler_select_combobox.clear()
        for sampler in self.image_settings_tab.samplers.values():
            if model_name in sampler["valid_for_model"]:
                samplers.append(sampler["name"])

        self.image_settings_tab.sampler_select_combobox.addItems(samplers)
            
        if stored_sampler in samplers:
            self.image_settings_tab.sampler_select_combobox.setCurrentText(stored_sampler)
        elif samplers:
            self.image_settings_tab.sampler_select_combobox.setCurrentText(samplers[0])

        self.image_settings_tab.update_sampler_properties()

        schedules = []
        stored_schedule = self.image_settings_tab.schedule_select_combobox.currentText()
        self.image_settings_tab.schedule_select_combobox.clear()
        for schedule in self.image_settings_tab.schedules.values():
            if model_name in schedule["valid_for_model"]:
                schedules.append(schedule["name"])

        self.image_settings_tab.schedule_select_combobox.addItems(schedules)
            
        if stored_schedule in schedules:
            self.image_settings_tab.schedule_select_combobox.setCurrentText(stored_schedule)
        elif schedules:
            self.image_settings_tab.schedule_select_combobox.setCurrentText(schedules[0])

        self.image_settings_tab.update_schedule_properties()



        

 
   

