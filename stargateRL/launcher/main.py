"""The main launcher for changing the configurations."""

import os
import sys
import tkinter as tki

from stargateRL.launcher import elements
from stargateRL.launcher.utils import load_config, save_config
from stargateRL.paths import DirectoryPaths


def launch():
    """Start the stargateRL.__main__ method."""
    root.destroy()

    # TODO: Make a top import of main() and use it here
    import stargateRL.main
    stargateRL.main.main()


def match():
    """Check if the existing config matches the launcher config."""
    save(write=False)
    return CONFIG == load_config()


def save(write=True):
    """Method called by the Apply button."""
    config_dictionary = CONFIG
    for _section in CONFIG.keys():
        for _key in CONFIG[_section].keys():
            config_dictionary[_section][_key] =\
                config_frame.subframes[_section].options[_key].get_value()
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
        popup = tki.Toplevel(master=None)
        popup.title('Are you sure?')
        popup.resizable(0, 0)

        popup.grab_set()

        label = tki.Label(popup, anchor=tki.N,
                          text='Are you sure you want to exit without saving?')
        label.pack(side=tki.TOP, fill=tki.X)

        tki.Button(popup, anchor=tki.CENTER, text='Yes',
                   command=root.destroy).pack(side=tki.LEFT)
        tki.Button(popup, anchor=tki.CENTER, text='No',
                   command=popup.destroy).pack(side=tki.LEFT)

        popup.mainloop()
        try:
            popup.destroy()
        except Exception:
            sys.exit()


CONFIG = load_config()
root = tki.Tk()

root.resizable(0, 0)
root.wm_title('stargateRL Launcher')

# GUI goes bellow this line
# Generate the sections
config_frame = elements.MainFrame(root)
config_frame.make_subframes(CONFIG.keys())

TILE_PATH = DirectoryPaths.TILES.value
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
                        config_frame.subframes[section],
                        key, value, TILESETS)
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

tki.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
           text='Apply', command=save).pack(side=tki.LEFT, fill=tki.X)
tki.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
           text='Cancel', command=close).pack(side=tki.LEFT, fill=tki.X)
tki.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
           text='Default', command=default).pack(side=tki.LEFT, fill=tki.X)
tki.Button(config_frame, highlightbackground=elements.MAINFRAME_COLORS[0],
           text='Launch', command=launch).pack(side=tki.RIGHT, fill=tki.X)

# GUI goes above this line
root.mainloop()
try:
    root.destroy()
except Exception:
    sys.exit()
