"""A set of GUI elements for the launcher."""

import Tkinter as tk

SUBFRAMES_TITLES = ['GRAPHICS', 'WINDOW', 'RESOURCES']


class MainFrame(tk.Frame):
    """The main frame element."""

    def __init__(self, master):
        """Construct the main frame."""
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH)

        self._subframes = {}

    def make_subframes(self, frames):
        """Generate empty subframes for the settings."""
        for frame in frames:
            self._subframes[frame] = SubFrame(self, frame)


class SubFrame(tk.Frame):
    """A section of settings."""

    def __init__(self, master, label):
        """Construct the sub frame."""
        tk.Frame.__init__(self, master)
        self.pack(side=tk.TOP, fill=tk.BOTH)

        self._label = tk.Label(master=self, text='# '+label, anchor=tk.NW,
                               padx=5)
        self._label.pack(fill=tk.X)


# TODO: Combine Inputs into one class and inherit from there
# possibly...
class IntegerInput(tk.Frame):
    """Input a integer."""

    def __init__(self, master, label, value, positive=True):
        """Construct the integer input."""
        tk.Frame.__init__(self, master)
        self.pack(side=tk.TOP, fill=tk.X)

        self._label = tk.Label(master=self, text=label+':', anchor=tk.W,
                               padx=30, width=10)
        self._label.pack(fill=tk.X, side=tk.LEFT)

        self._value = tk.StringVar(value=value)
        self._entry = tk.Entry(master=self, textvariable=self._value)
        self._entry.pack(fill=tk.X, side=tk.RIGHT)


class BooleanInput(tk.Frame):
    """Input a boolean."""

    def __init__(self, master, label, value):
        """Construct the boolean input."""
        tk.Frame.__init__(self, master)
        self.pack(side=tk.TOP, fill=tk.X)

        self._label = tk.Label(master=self, text=label+':', anchor=tk.W,
                               padx=30, width=10)
        self._label.pack(fill=tk.X, side=tk.LEFT)

        self._value = tk.BooleanVar(value=value)
        self._entry = tk.Checkbutton(master=self, variable=self._value,
                                     onvalue=True, offvalue=False)
        self._entry.pack(fill=tk.X, side=tk.LEFT)
