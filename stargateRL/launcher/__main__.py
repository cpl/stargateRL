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


def save():
    """Method called by the Apply button."""
    pass


def default():
    """Change the configs back to the default."""
    pass


def close():
    """Method called by the Close button."""
    popup = tk.Toplevel(master=None)
    popup.title('Are you sure?')
    popup.resizable(0, 0)

    popup.grab_set()

    label = tk.Label(popup, anchor=tk.N,
                     text='Are you sure you want to exit without saving?')
    label.pack(side=tk.TOP, fill=tk.X)

    tk.Button(popup, anchor=tk.CENTER, text='Yes',
              command=root.destroy).pack(side=tk.LEFT)
    tk.Button(popup, anchor=tk.CENTER, text='No',
              command=popup.destroy).pack(side=tk.LEFT)

    popup.mainloop()
    popup.destroy()


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

tk.Button(mf, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Apply').pack(side=tk.LEFT, fill=tk.X)
tk.Button(mf, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Cancel', command=close).pack(side=tk.LEFT, fill=tk.X)
tk.Button(mf, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Default', command=default).pack(side=tk.LEFT, fill=tk.X)

# GUI goes above this line
root.mainloop()
root.destroy()
