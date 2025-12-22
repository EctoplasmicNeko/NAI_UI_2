import math
import sys

from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from PySide6.QtCore import QTimer, QThread

from widget.dropawareframe import DropAwareFrame
from process.CompletionSignaler import completion_signaler
from data.datahub import get_data, load_image_tree
from windows.error import Error
from windows.import_on_drop import ImportDialog
from signaling.import_signal import import_signal

from ui.columns.left_column import LeftColumn
from ui.columns.centre_column import CentreColumn
from ui.columns.right_column import RightColumn
from process.workers import GenerateWorker
from data.save import load_config, save_config
from process.drop_handling import get_metadata, is_valid_image_file
from windows.manage_characters import ManageCharacterWindow
from data.paths import THEMES_DIR


class MainUI(DropAwareFrame):
    def __init__(self, ):
        super().__init__(parent=None, on_files_dropped=self.file_dropped)

        self.import_dialgue_settings_state = False
        self.import_dialgue_prompt_state = False
        self.import_dialgue_seed_state = False
        self.import_dialgue_characters_state = False

        self.image_cache = load_image_tree()
        print(self.image_cache['references'])
        self.build_main_ui()
        loaded_config = load_config()
        self.left_column_widget.refresh_all_character_lists()
        self.setWindowTitle("NAI UI 2")
        self.restore_ui_state(loaded_config)
        
        self.models = get_data("models") #load the models dictionary from the data cache
        self.schedulers = get_data("schedules") #load the models dictionary from the data cache
        self.samplers = get_data("samplers") #load the models dictionary from the data cache
        self.sizes = get_data("sizes") #load the sizes dictionary from the data cache

        self.loops = 0
        self.sets = 0
        self.total_loops = 0
        self.requested_loops = 0
        self.requested_sets = 0
        self.new_request = True
        self.incriment_set = False

    def build_main_ui(self):
        self.main_grid_layout = QGridLayout(self)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setSpacing(0)

        self.left_column_widget = LeftColumn(self, self.image_cache)
        self.centre_column_widget = CentreColumn(self)
        self.right_column_widget = RightColumn(self)

        self.main_grid_layout.addWidget(self.left_column_widget, 0, 0)
        self.main_grid_layout.addWidget(self.centre_column_widget, 0, 1)
        self.main_grid_layout.addWidget(self.right_column_widget, 0, 2)

        self.main_grid_layout.setColumnStretch(0, 1)
        self.main_grid_layout.setColumnStretch(1, 3)
        self.main_grid_layout.setColumnStretch(2, 1)
        self.main_grid_layout.setRowStretch(0, 1)

        #Bound buttons
        self.left_column_widget.upper_frame.page4.generate_button.pressed.connect(lambda: self.core_loop())
        self.left_column_widget.upper_frame.page4.test_button.pressed.connect(lambda: self.abort_loops())
        self.left_column_widget.upper_frame.page4.manage_characters_button.pressed.connect(lambda: self.launch_manage_characters())
        self.centre_column_widget.viewport_button.pressed.connect(lambda: self.core_loop())
        self.left_column_widget.upper_frame.page4.theme_combo.currentIndexChanged.connect(lambda: self.apply_theme(QApplication.instance(), self.left_column_widget.upper_frame.page4.theme_combo.currentText()))
        import_signal.import_signal.connect(self.import_state_from_image_metadata)
        self.left_column_widget.upper_frame.page2.cancel_task_button.pressed.connect(lambda: self.abort_loops())

    def file_dropped(self, file_path):
        if not is_valid_image_file(file_path):
            Error(self, "The dropped file is not a supported image format.")
            return
        
        dict_type, metadata = get_metadata(file_path)
        if not metadata:
            Error(self, "No valid metadata found in the dropped image.")
            return
        
        import_dialog = ImportDialog(self, file_path, dict_type, metadata, self.import_dialgue_settings_state, self.import_dialgue_prompt_state, self.import_dialgue_seed_state, self.import_dialgue_characters_state)
        import_dialog.exec()

      

    def get_ui_state(self):
        state = {
        'main_window': self.export_state(),
        'generate': self.left_column_widget.upper_frame.page0.image_master_stack_generate.export_state(),
        'colorize': self.left_column_widget.upper_frame.page0.image_master_stack_colorize.export_state(),
        'emotion': self.left_column_widget.upper_frame.page0.image_master_stack_emotion.export_state(),
        'global_prompt': self.left_column_widget.upper_frame.page1.export_state(),
        'workflow': self.left_column_widget.upper_frame.page2.export_state(),
        'settings': self.left_column_widget.upper_frame.page4.export_state(),
        
        'character_1': self.left_column_widget.middle_frame.character_tab_1.export_state() | self.left_column_widget.lower_frame.character_tab_1.export_state(),
        'character_2': self.left_column_widget.middle_frame.character_tab_2.export_state() | self.left_column_widget.lower_frame.character_tab_2.export_state(),
        'character_3': self.left_column_widget.middle_frame.character_tab_3.export_state() | self.left_column_widget.lower_frame.character_tab_3.export_state(),
        'character_4': self.left_column_widget.middle_frame.character_tab_4.export_state() | self.left_column_widget.lower_frame.character_tab_4.export_state(),
        'character_5': self.left_column_widget.middle_frame.character_tab_5.export_state() | self.left_column_widget.lower_frame.character_tab_5.export_state()
        }
        return state
    
    def check_loop_conditions(self):
        if self.new_request:
            self.loops = 0
            self.sets = 0
            self.total_loops = 0

            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_loop_bar.setValue(0)
            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_set_bar.setValue(0)

            completion_signaler.start_signal.emit()
            self.requested_loops = self.left_column_widget.upper_frame.page2.loops.value()
            self.requested_sets = self.left_column_widget.upper_frame.page2.sets.value()
            if self.requested_sets == 0: #use 'per character' mode
                self.requested_sets = self.left_column_widget.upper_frame.page2.determine_list_length()

            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_loop_bar.setRange(0, self.requested_loops)
            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_set_bar.setRange(0, self.requested_sets)
            self.left_column_widget.upper_frame.page2.loops.setDisabled(True)
            self.left_column_widget.upper_frame.page2.sets.setDisabled(True)
            self.new_request = False
    
    def abort_loops(self):
        print("Aborting loops...")
        self.loops = 0
        self.sets = 0
        self.total_loops = 0
        self.left_column_widget.upper_frame.page2.loops.setDisabled(False) 
        self.left_column_widget.upper_frame.page2.sets.setDisabled(False)
        self.new_request = True
        
        completion_signaler.complete_signal.emit()
        

    def core_loop(self):
        if self.incriment_set:
            self.incriment_set = False
            self.loops = 0
            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_loop_bar.setValue(self.loops)
            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_set_bar.setValue(self.sets)
            

        completion_signaler.window_lock_signal.emit(True)
        self.check_loop_conditions()
        completion_signaler.loop_start_signal.emit(self.left_column_widget.upper_frame.page2.list.item(0).text())
        state = self.get_ui_state()
        self.generate_thread = QThread(self)
        self.generate_worker = GenerateWorker(state)
        self.generate_worker.moveToThread(self.generate_thread)
        self.generate_thread.started.connect(self.generate_worker.run)
        self.generate_worker.result.connect(self.on_generate_result)
        self.generate_worker.finished.connect(self.generate_thread.quit)
        self.generate_worker.finished.connect(self.generate_worker.deleteLater)
        self.generate_thread.finished.connect(self.generate_thread.deleteLater)
        self.generate_thread.start()

    def on_generate_result(self, image_path: str, state: dict):
        print(f'Generation result received: {image_path}')
        if image_path == '':
            Error(self, "Generation failed. Please check your settings and try again.")
            return
        
        else:
            self.centre_column_widget.update_image(image_path)
            self.left_column_widget.upper_frame.page2.cycle_list()
            
            self.setProperty("most_recent_image", image_path)
            self.setProperty("most_recent_width", state['generate']["image_width"])
            self.setProperty("most_recent_height", state['generate']["image_height"])

            self.loops += 1
            self.total_loops += 1
            self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_loop_bar.setValue(self.loops)
            if self.loops >= self.requested_loops:
                self.incriment_set = True
                self.sets += 1
                completion_signaler.set_start_signal.emit()

            if self.loops <= self.requested_loops and self.sets < self.requested_sets:
                completion_signaler.window_lock_signal.emit(False)
                
            elif self.loops >= self.requested_loops and self.sets >= self.requested_sets:
                self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_loop_bar.setValue(self.loops)
                self.left_column_widget.upper_frame.page0.image_master_stack_generate.image_settings_tab.generate_progress_set_bar.setValue(self.sets)
                print(f"All loops and sets completed. Total loops executed: {self.total_loops}")

                self.left_column_widget.upper_frame.page2.loops.setDisabled(False) 
                self.left_column_widget.upper_frame.page2.sets.setDisabled(False)
                self.new_request = True
                completion_signaler.complete_signal.emit()
          

    def restore_ui_state(self, loaded):
        self.import_state(loaded['main_window'])
        self.left_column_widget.upper_frame.page0.image_master_stack_generate.import_state(loaded['generate'])
        self.left_column_widget.upper_frame.page0.image_master_stack_colorize.import_state(loaded['colorize'])
        self.left_column_widget.upper_frame.page0.image_master_stack_emotion.import_state(loaded['emotion'])
        self.left_column_widget.upper_frame.page1.import_state(loaded['global_prompt'])
        self.left_column_widget.upper_frame.page2.import_state(loaded['workflow'])
        self.left_column_widget.upper_frame.page4.import_state(loaded['settings']),

        self.left_column_widget.middle_frame.character_tab_1.import_state(loaded['character_1'])
        self.left_column_widget.middle_frame.character_tab_2.import_state(loaded['character_2'])
        self.left_column_widget.middle_frame.character_tab_3.import_state(loaded['character_3'])
        self.left_column_widget.middle_frame.character_tab_4.import_state(loaded['character_4'])
        self.left_column_widget.middle_frame.character_tab_5.import_state(loaded['character_5'])

        self.left_column_widget.lower_frame.character_tab_1.import_state(loaded['character_1'])
        self.left_column_widget.lower_frame.character_tab_2.import_state(loaded['character_2'])
        self.left_column_widget.lower_frame.character_tab_3.import_state(loaded['character_3'])
        self.left_column_widget.lower_frame.character_tab_4.import_state(loaded['character_4'])
        self.left_column_widget.lower_frame.character_tab_5.import_state(loaded['character_5'])

        theme_name = self.left_column_widget.upper_frame.page4.theme_combo.currentText()
        self.apply_theme(QApplication.instance(), theme_name)


    def export_state(self):
        return {
            'most_recent_image': self.property('most_recent_image'),
            'most_recent_height': self.property('most_recent_height'),
            'most_recent_width': self.property('most_recent_width'),
            'import_dialog_settings_state': self.import_dialgue_settings_state,
            'import_dialog_prompt_state': self.import_dialgue_prompt_state,
            'import_dialog_seed_state': self.import_dialgue_seed_state,
            'import_dialog_characters_state': self.import_dialgue_characters_state,
        }
    
    def import_state(self, loaded):
        self.setProperty("most_recent_image", loaded['most_recent_image'])
        self.setProperty("most_recent_width", loaded['most_recent_width'])
        self.setProperty("most_recent_height", loaded['most_recent_height'])
        self.import_dialgue_settings_state = loaded['import_dialog_settings_state']
        self.import_dialgue_prompt_state = loaded['import_dialog_prompt_state']
        self.import_dialgue_seed_state = loaded['import_dialog_seed_state']
        self.import_dialgue_characters_state = loaded['import_dialog_characters_state']

    def closeEvent(self, event):
        state = self.get_ui_state()
        save_config(state)
        event.accept()

    def launch_manage_characters(self):
        self.manage_char_window = ManageCharacterWindow(self, self.image_cache)
        self.manage_char_window.exec()
        self.image_cache = load_image_tree()
        self.left_column_widget.middle_frame.character_tab_1.image_cache = self.image_cache
        self.left_column_widget.middle_frame.character_tab_2.image_cache = self.image_cache
        self.left_column_widget.middle_frame.character_tab_3.image_cache = self.image_cache
        self.left_column_widget.middle_frame.character_tab_4.image_cache = self.image_cache
        self.left_column_widget.middle_frame.character_tab_5.image_cache = self.image_cache
        #refresh of character lists will be handled by signal emitted from manage characters window
        

    def import_state_from_image_metadata(self, dict_type: str, metadata: dict, load_settings: bool, 
                                         load_prompt: bool, load_seed: bool, load_characters: bool):
        
        print("Importing state from image metadata...")
        self.import_dialgue_prompt_state = load_prompt
        self.import_dialgue_settings_state = load_settings
        self.import_dialgue_seed_state = load_seed
        self.import_dialgue_characters_state = load_characters

        state = self.get_ui_state()

        if dict_type == 'custom':
            
                if load_settings:
                    #generate
                    state['generate']['model_name'] = metadata['generate']['model']
                    state['generate']['sampler_name'] = metadata['generate']['sampler']
                    state['generate']['schedule_name'] = metadata['generate']['schedule']
                    state['generate']['steps'] = metadata['generate']['steps']
                    state['generate']['scale'] = metadata['generate']['scale']  
                    state['generate']['rescale'] = metadata['generate']['rescale']
                    state['generate']['cfg'] = metadata['generate']['cfg']

                    state['generate']['legacy_v3'] = metadata['generate']['legacy_v3']
                    state['generate']['legacy_v4'] = metadata['generate']['legacy_v4']
                    state['generate']['SMEA'] = metadata['generate']['SMEA']
                    state['generate']['DYN'] = metadata['generate']['DYN']
                    state['generate']['variety+'] = metadata['generate']['variety+']
                    state['generate']['decrisp'] = metadata['generate']['decrisp']
                    state['generate']['brownian'] = metadata['generate']['brownian']

                    state['generate']['size_name'] = metadata['generate']['size_name']

                if load_seed:
                    state['generate']['seed'] = metadata['generate']['seed']

                    #characters     
                if load_characters:
                    character_number = metadata['global_prompt']['character_number']
                    for index in range(1, character_number + 1):
                        key = f"character_{index}"

                        state[key]['character'] = metadata['characters'][key]['character']

                        state[key]['character_positive_prompt'] = metadata['characters'][key]['character_positive_prompt']
                        state[key]['character_negative_prompt'] = metadata['characters'][key]['character_negative_prompt']
                        state[key]['character_preset_positive'] = metadata['characters'][key]['character_preset_positive']
                        state[key]['character_preset_negative'] = metadata['characters'][key]['character_preset_negative'] 
                        state[key]['character_preset_global_positive'] = metadata['characters'][key]['character_preset_global_positive']
                        state[key]['character_preset_global_negative'] = metadata['characters'][key]['character_preset_global_negative']
                        state[key]['character_coordinate_button'] = metadata['characters'][key]['character_coordinate_button']
                        state[key]['character_outfit_preset_positive'] = metadata['characters'][key]['character_outfit_preset_positive']
                        state[key]['character_outfit_preset_negative'] = metadata['characters'][key]['character_outfit_preset_negative']
                        state[key]['most_recent_outfit'] = metadata['characters'][key]['most_recent_outfit']

                if load_prompt:
                    #global prompt
                    state['global_prompt']['global_positive_prompt'] = metadata['global_prompt']['global_positive_prompt']
                    state['global_prompt']['global_negative_prompt'] = metadata['global_prompt']['global_negative_prompt']
                    state['global_prompt']['global_positive_preset_name'] = metadata['global_prompt']['global_positive_preset_name']
                    state['global_prompt']['global_negative_preset_name'] = metadata['global_prompt']['global_negative_preset_name']
                    state['global_prompt']['global_positive_preset_tags'] = metadata['global_prompt']['global_positive_preset_tags']
                    state['global_prompt']['global_negative_preset_tags'] = metadata['global_prompt']['global_negative_preset_tags']
                    state['global_prompt']['character_number'] = metadata['global_prompt']['character_number']
                
        else:
            if dict_type == 'native':
                    
                if load_settings:

                    model_used = metadata['top_level']['source']
                    matched_model = None
                    for model in self.models.values():
                        builds = model.get("builds", [])
                        inpaints = model.get("inpaints", [])

                        if model_used in builds or model_used in inpaints:
                            matched_model = model
                            break

                    if matched_model is None:
                        Error(self, "The model used to generate this image is not mapped. Please contact u/EctoplasmicNeko on Reddit to have it added.")
                        return

                    state['generate']['model_name'] = matched_model["name"]
                    
                    sampler_used = metadata['generate']['sampler']
                    for sampler in self.samplers.values():
                        if sampler_used == sampler["payload_name"]:
                            state['generate']['sampler_name'] = sampler["name"]

                    schedule_used = metadata['generate']['noise_schedule']
                    for schedule in self.schedulers.values():
                        if schedule_used == schedule["payload_name"]:
                            state['generate']['schedule_name'] = schedule["name"]
                        
                    state['generate']['steps'] = metadata['generate']['steps']
                    state['generate']['scale'] = metadata['generate']['scale'] 

                    state['generate']['rescale'] = metadata['generate']['cfg_rescale']

                    used_cfg = metadata['generate']['skip_cfg_above_sigma']
                    if used_cfg is None:
                        used_cfg = -1
                    state['generate']['cfg'] = used_cfg

                    state['generate']['legacy_v3'] = metadata['generate']['legacy_v3_extend']
                    state['generate']['legacy_v4'] = metadata['generate']['legacy_uc']
                    state['generate']['SMEA'] = metadata['generate']['sm']
                    state['generate']['DYN'] = metadata['generate']['sm_dyn']
                    state['generate']['variety+'] = False
                    state['generate']['decrisp'] = metadata['generate']['dynamic_thresholding']
                    state['generate']['brownian'] = metadata['generate']['prefer_brownian']

                    used_height = metadata['generate']['height']
                    used_width = metadata['generate']['width']

                    for size in self.sizes:
                        if size['image_height'] == used_height and size['image_width'] == used_width:
                            state['generate']['size_name'] = size['name']
                            break
                    else:
                        state['generate']['size_name'] = None
                        state['generate']['image_height'] = used_height
                        state['generate']['image_width'] = used_width

                if load_seed:
                    state['generate']['seed'] = metadata['generate']['seed']

                if load_characters:
                    character_number = metadata['global_prompt']['character_number']
                    for index in range(1, character_number + 1):
                        key = f"character_{index}"
                        state[key]['character'] = 'Loaded'  #trigger for character matching screen  

                        state[key]['character_positive_prompt'] = metadata['characters'][key]['character_positive_prompt']
                        state[key]['character_negative_prompt'] = metadata['characters'][key]['character_negative_prompt']
                        state[key]['character_preset_positive'] = None
                        state[key]['character_preset_negative'] = None
                        state[key]['character_preset_global_positive'] = None
                        state[key]['character_preset_global_negative'] = None

                        x = metadata['characters'][key]['character_x_pos']
                        y = metadata['characters'][key]['character_y_pos']
                        state[key]['character_coordinate_button'] = self.coord_to_button_id(x, y)

                if load_prompt:
                    #global prompt
                    state['global_prompt']['global_positive_prompt'] = metadata['global_prompt']['global_positive_prompt']
                    state['global_prompt']['global_negative_prompt'] = metadata['global_prompt']['global_negative_prompt']
                    state['global_prompt']['global_positive_preset_name'] = 'None'
                    state['global_prompt']['global_negative_preset_name'] = 'None'
                    state['global_prompt']['global_positive_preset_tags'] = ''
                    state['global_prompt']['global_negative_preset_tags'] = ''
                    state['global_prompt']['character_number'] = metadata['global_prompt']['character_number']
                    

        self.restore_ui_state(state)


    def coord_to_index_floor(self, coord: float) -> int:
        # Special-case "None" sentinel
        if coord == 0.0:
            return -1

        raw_index = (coord - 0.1) / 0.2
        index = int(math.floor(raw_index + 1e-6))
        return max(0, min(4, index))  # Clamp to [0, 4]


    def coord_to_button_id(self, x: float, y: float) -> int:
        # (0,0) means "None" -> ID 0
        if x == 0.0 and y == 0.0:
            return 0

        col = self.coord_to_index_floor(x)  # 0 = left
        row = self.coord_to_index_floor(y)  # 0 = bottom
        return row * 5 + col + 1  # 1-based ID


    def apply_theme(self, app, theme_name):
        theme_path = THEMES_DIR / f"{theme_name}.qss"
        with open(theme_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

def run_app():
    app = QApplication(sys.argv)
    window = MainUI()
    window.showMaximized()   # show it maximized
    sys.exit(app.exec())
