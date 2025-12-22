from data.datahub import get_all_characters
from process.CompletionSignaler import completion_signaler  
from signaling.cycle_character import cycle_character_signal
import random

class CharacterAutoCycleManager():

    def __init__(self, parent, current_character):
        self.parent = parent
        self.characters = get_all_characters()
        self.cycle_tag1 = None
        self.cycle_tag2 = None
        self.base_character_list = []
        self.character_list = []
        self.current_index = 0
        self.counter = 0
        self.new_list = False
        self.current_operation = None
        self.current_character = current_character
        self.set_cycled = False

        completion_signaler.loop_start_signal.connect(self.on_loop_start)
        completion_signaler.set_start_signal.connect(lambda: setattr(self, 'set_cycled', True))

    def on_loop_start(self, action_type: str):
        if action_type == "Generate":
            self.check_operate_cycle()

    def check_operate_cycle(self):
        tab4 = self.parent.sub_notebook.character_sub_tab_4

        if tab4.auto_advance_characters_checkbox.isChecked():
            self.current_operation = "auto_cycle"

        elif tab4.auto_random_characters_checkbox.isChecked():
            self.current_operation = "auto_random"

            
        if self.current_operation == "auto_random" or self.current_operation == "auto_cycle":
        
            self.selected_cycle_tag1 = tab4.auto_advance_character_tag1_combo.currentText()
            self.selected_cycle_tag2 = tab4.auto_advance_character_tag2_combo.currentText()
            self.frequency = tab4.auto_advance_character_frequency_spinbox.value()

            if (self.cycle_tag1 != self.selected_cycle_tag1 or
                self.cycle_tag2 != self.selected_cycle_tag2):

                self.cycle_tag1 = self.selected_cycle_tag1
                self.cycle_tag2 = self.selected_cycle_tag2
                self.character_list = []
                self.current_index = 0
                self.counter = 0
                self.build_list()

            self.counter += 1

            if self.frequency != 0:
                self.set_cycled = False
                if self.counter > self.frequency:
                    if self.current_operation == "auto_cycle":
                        if self.new_list:
                            self.current_index = 0
                            self.new_list = False
                        else:
                            self.current_index = (self.current_index + 1) % len(self.character_list)

                        self.counter = 1
                        cycle_character_signal.character_cycle_signal.emit(
                            self.character_list[self.current_index],
                            self.parent.ID
                        )
                        print(f"Cycled to character: {self.character_list[self.current_index]}")

                    elif self.current_operation == "auto_random":
                        selected_character = random.choice(self.character_list)
                        self.counter = 0
                        cycle_character_signal.character_cycle_signal.emit(
                            selected_character,
                            self.parent.ID
                        )
                        print(f"Randomly selected character: {selected_character}")
            
                else:
                    print(f"cycles remaining until next character: {self.frequency - self.counter}")

            elif self.frequency == 0: #Utilizes `On Set` functionality
                if self.set_cycled:
                    print(f"Set cycle flag is true, cycling character this generation.")
                    if self.current_operation == "auto_cycle":
                            if self.new_list:
                                self.current_index = 0
                                self.new_list = False
                                self.set_cycled = False
                            else:
                                self.current_index = (self.current_index + 1) % len(self.character_list)

                            self.counter = 1
                            cycle_character_signal.character_cycle_signal.emit(
                                self.character_list[self.current_index],
                                self.parent.ID
                            )
                            print(f"Cycled to character: {self.character_list[self.current_index]}")
                            self.set_cycled = False

                    elif self.current_operation == "auto_random":
                        selected_character = random.choice(self.character_list)
                        self.counter = 0
                        cycle_character_signal.character_cycle_signal.emit(
                            selected_character,
                            self.parent.ID
                        )
                        print(f"Randomly selected character: {selected_character}")
                        self.set_cycled = False
            
                else:
                    print(f"Set cycle flag is false, not cycling character this generation.")

        else:
            self.cycle_tag1 = None
            self.cycle_tag2 = None
            self.character_list = []
            self.current_index = 0
            self.counter = 0
            self.new_list = False
            self.current_operation = None
        

    def build_list(self):
        print("Building character list for auto-cycle...")
        self.new_list = True
        self.character_list = self.base_character_list.copy()

        for character in self.characters:
            if self.cycle_tag1 !='None' and self.cycle_tag2 !='None':
                if self.cycle_tag1 not in character['tags'] and self.cycle_tag2 not in character['tags']:
                    self.character_list.remove(character)
            elif self.cycle_tag1 !='None' and self.cycle_tag2 =='None':
                if self.cycle_tag1 not in character['tags']:
                    self.character_list.remove(character)
            elif self.cycle_tag1 =='None' and self.cycle_tag2 !='None':
                if self.cycle_tag2 not in character['tags']:
                    self.character_list.remove(character)
            else:
                pass
        print(f"Auto-cycle character list built with {len(self.character_list)} characters.")
    



        

        