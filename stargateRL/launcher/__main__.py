"""The main launcher for changing the configurations."""


import json
import os
import tkinter as tk

from stargateRL.launcher import elements


def load_config():
    """Load the config file."""
    # Check local config first
    config_file_name = 'config.json'
    if os.path.isfile('config.local.json'):
        config_file_name = 'config.local.json'
    with open(config_file_name, 'r') as config_file:
        return json.load(config_file)


def save_config(config_dictionary):
    """Save the config changes."""
    config_file_name = 'config.json'
    if os.path.isfile('config.local.json'):
        config_file_name = 'config.local.json'
    with open(config_file_name, 'w') as config_file:
        json.dump(config_dictionary, config_file, indent=4)


def set_config(section, key, value):
    """Set the value of the section."""
    CONFIG[section][key] = value


root = tk.Tk()
root.resizable(0, 0)
root.wm_title('StargateRL Launcher')

CONFIG = load_config()

# GUI goes bellow this line

# Generate the sections
mf = elements.MainFrame(root)
mf.make_subframes(CONFIG.keys())

# Fill the sections with options
for section in CONFIG.keys():
    for key, value in CONFIG[section].items():
        value_type = type(value)
        if value_type == int:
            mf.subframes[section].options.append(
                elements.IntegerInput(mf.subframes[section], key, value))
        elif value_type == bool:
            mf.subframes[section].options.append(
                elements.BooleanInput(mf.subframes[section], key, value))
        elif value_type == str or value_type == unicode:
            mf.subframes[section].options.append(
                elements.StringInput(mf.subframes[section], key, value))

tk.Button(mf, text='Apply', fg='#DF6140').pack(side=tk.LEFT, fill=tk.X)
tk.Button(mf, text='Cancel', fg='#DF6140').pack(side=tk.LEFT, fill=tk.X)


# GUI goes above this line
root.mainloop()
root.destroy()
