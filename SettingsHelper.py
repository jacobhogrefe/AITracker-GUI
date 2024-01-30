'''
All of the necessary functions for the settings screen should be located in here.
'''
import customtkinter as ctk
import json
import re

class SettingsOption(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        
        #setting widgets
        self._name = name
        self.label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self.switch_var = ctk.BooleanVar(value=True)
        self.switch = ctk.CTkSwitch(self, variable=self.switch_var, onvalue=True, offvalue=False, text="Active")
        
        self.input_var = ctk.StringVar(value="")
        self.input = ctk.CTkEntry(self, textvariable=self.input_var)
        self.input.bind("<KeyRelease>", self.validate_pin)
        
        self.check_var = ctk.BooleanVar(value=False)
        self.check = ctk.CTkCheckBox(self, variable=self.check_var, onvalue=True, offvalue=False, text="Constant Input")
        
        #setting placements
        self.label.grid(row=0, column=0, padx=5, pady=5)
        self.switch.grid(row=0, column=1, padx=5, pady=5)
        self.input.grid(row=1, column=0, padx=5, pady=5)
        self.check.grid(row=1, column=1, padx=5, pady=5)
    
    @property
    def name(self) -> str:
        return self._name
        
    def validate_pin(self, *args):
        if re.match("^C[1-9]$|^D[0-7]$", self.input_var.get().strip()):
            self.input.configure(text_color="green")
        else:
            self.input.configure(text_color="red")
        return True;
    
    # returns a dictionary mapping for the setting name, and all of the values  
    def get_settings(self):
        return (self.switch_var.get(), self.input_var.get(), self.check_var.get())
    
    # sets the settings
    def set_settings(self, settings):
        self.switch_var.set(settings[0])
        self.input_var.set(settings[1])
        self.check_var.set(settings[2])

class NumberEntry(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        validate_cmd = root.register(self.validate_input)
        self.name = name
        
        # widgets
        label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self.entry_var = ctk.StringVar(value="0")
        entry = ctk.CTkEntry(self, textvariable=self.entry_var, validate="key", validatecommand=(validate_cmd, "%P"))
        
        # placements
        label.grid(row=0, column=0, padx=5, pady=5)
        entry.grid(row=1, column=0, padx=5, pady=5)
    
    # validates that only a number can be an input to the field
    def validate_input(self, new_value):
        try:
            if new_value == "":
                return True
            
            float(new_value)
            return True
        except ValueError:
            return False
    
    def get_value(self):
        return {self.name:int(self.entry_var.get())}
        
    def set_value(self, input_value):
        self.entry_var.set(str(input_value))

def load_settings(json_path):
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        # convert arrays to tuples
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = tuple(value)

        return data
    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{json_path}'.")
        return {}

def save_settings_to_json(settings_dict, json_path):
    try:
        with open(json_path, 'w') as json_file:
            json.dump(settings_dict, json_file, indent=2)
    except Exception as e:
        print(f"Error saving data to '{json_path}': {e}")