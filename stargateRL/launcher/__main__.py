"""The main launcher for changing the configurations."""


import json
import os
import tkinter as tk

from stargateRL.launcher import elements


def launch():
    """Start the stargateRL.__main__ method."""
    root.destroy()
    import stargateRL.__main__


def load_config():
    """Load the config file."""
    config_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     os.pardir, os.pardir, 'config.json'))
    with open(config_file_name, 'r') as config_file:
        return json.load(config_file)


def save_config(config_dictionary):
    """Save the config changes."""
    config_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     os.pardir, os.pardir, 'config.json'))
    with open(config_file_name, 'w') as config_file:
        json.dump(config_dictionary, config_file, indent=4, sort_keys=True)


def match():
    """Check if the existing config matches the launcher config."""
    save(False)
    print CONFIG == load_config()
    return CONFIG == load_config()


def save(write=True):
    """Method called by the Apply button."""
    config_dictionary = CONFIG
    for section in CONFIG.keys():
        for key, value in CONFIG[section].items():
            config_dictionary[section][key] =\
                config_frame.subframes[section].options[key].get_value()
    if write:
        save_config(config_dictionary)


def default():
    """Change the configs back to the default."""
    pass


def close():
    """Method called by the Close button."""
    if match():
        root.destroy()
    else:
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
root.wm_title('stargateRL Launcher')

CONFIG = load_config()

# GUI goes bellow this line
# Generate the sections
config_frame = elements.MainFrame(root)
config_frame.make_subframes(CONFIG.keys())

TILE_PATH = os.path.abspath(os.path.join(os.path.join(
    __file__, os.pardir, os.pardir, os.pardir, 'bin', 'tiles')))
TILESETS = [tile for tile in os.listdir(TILE_PATH) if tile.endswith('.png')]
SIZES = [16, 20, 32, 64]

# Fill the sections with options
for section in CONFIG.keys():
    if section == 'audio':
        for key, value in CONFIG[section].items():
            config_frame.subframes[section].options[key] =\
                elements.Slider(
                    config_frame.subframes[section], key, value, 0, 100)
    else:
        for key, value in CONFIG[section].items():
            value_type = type(value)
            if key == 'tileset':
                config_frame.subframes[section].options[key] =\
                    elements.MultipleOptions(
                        config_frame.subframes[section], key, value, TILESETS)
            elif key == 'size':
                config_frame.subframes[section].options[key] =\
                    elements.MultipleOptions(
                        config_frame.subframes[section], key, value, SIZES)
            elif value_type == int:
                config_frame.subframes[section].options[key] =\
                    elements.IntegerInput(
                        config_frame.subframes[section], key, value)
            elif value_type == bool:
                config_frame.subframes[section].options[key] =\
                    elements.BooleanInput(
                        config_frame.subframes[section], key, value)
            elif value_type == str or value_type == unicode:
                config_frame.subframes[section].options[key] =\
                    elements.StringInput(
                        config_frame.subframes[section], key, value)

tk.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Apply', command=save).pack(side=tk.LEFT, fill=tk.X)
tk.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Cancel', command=close).pack(side=tk.LEFT, fill=tk.X)
tk.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Default', command=default).pack(side=tk.LEFT, fill=tk.X)

tk.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
          text='Launch', command=launch).pack(side=tk.RIGHT, fill=tk.X)

# GUI goes above this line
root.mainloop()
root.destroy()
