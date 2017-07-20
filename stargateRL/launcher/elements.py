"""A set of GUI elements for the launcher."""

import tkinter as tk
import tkinter.font as tkFont


# First color is the background, second color is the foreground
HEADER_COLORS = ('#37343E', '#F5EDEA')
VALUE_COLORS = ('', '#F5EDEA')
MAINFRAME_COLORS = ('#37343E', '')
SUBFRAME_COLORS = ('#7E7F7F', '')


class MainFrame(tk.Frame):
    """The main frame element."""

    def __init__(self, master):
        """Construct the main frame."""
        tk.Frame.__init__(self, master, bg=MAINFRAME_COLORS[0])
        self.pack(fill=tk.BOTH)

        self.subframes = {}

    def make_subframes(self, frames):
        """Generate empty subframes for the settings."""
        for frame in frames:
            self.subframes[frame] = SubFrame(self, frame)


class SubFrame(tk.Frame):
    """A section of settings."""

    def __init__(self, master, label):
        """Construct the sub frame."""
        tk.Frame.__init__(self, master, bg=SUBFRAME_COLORS[0])
        self.pack(side=tk.TOP, fill=tk.BOTH)
        self.options = {}

        header_font = tkFont.Font(family='Serif', size=18, weight=tkFont.BOLD)
        self._label = tk.Label(master=self, text='# '+label, anchor=tk.NW,
                               padx=25, font=header_font,
                               bg=HEADER_COLORS[0], fg=HEADER_COLORS[1])
        self._label.pack(fill=tk.X)


class Input(tk.Frame, object):
    """Standards for a input."""

    def __init__(self, master, label):
        """Construct standard input."""
        tk.Frame.__init__(self, master, bg=SUBFRAME_COLORS[0])
        self.pack(side=tk.TOP, fill=tk.X)

        self._label = tk.Label(master=self, text=label+':', anchor=tk.W,
                               padx=30, width=10, bg=SUBFRAME_COLORS[0])
        self._label.pack(fill=tk.X, side=tk.LEFT)

        self._value = None

    def get_value(self):
        """Return the value from the input."""
        return self._value


class IntegerInput(Input):
    """Input a integer."""

    def __init__(self, master, label, value):
        """Construct the integer input."""
        super(IntegerInput, self).__init__(master, label)

        self._value = tk.StringVar(value=value)
        self._entry = tk.Entry(master=self, textvariable=self._value,
                               bg=SUBFRAME_COLORS[0], relief=tk.FLAT,
                               highlightbackground=SUBFRAME_COLORS[0],
                               fg=VALUE_COLORS[1])
        self._entry.pack(fill=tk.X, side=tk.RIGHT)

    def get_value(self):
        """Return the value from the entry."""
        return int(self._entry.get())


class BooleanInput(Input):
    """Input a boolean."""

    def __init__(self, master, label, value):
        """Construct the boolean input."""
        super(BooleanInput, self).__init__(master, label)

        self._value = tk.BooleanVar(value=value)
        self._entry = tk.Checkbutton(master=self, variable=self._value,
                                     onvalue=True, offvalue=False,
                                     bg=SUBFRAME_COLORS[0])
        self._entry.pack(fill=tk.X, side=tk.LEFT)

    def get_value(self):
        """Return the value from the entry."""
        return self._value.get()


class StringInput(Input):
    """Input a string."""

    def __init__(self, master, label, value):
        """Construct the string input."""
        super(StringInput, self).__init__(master, label)

        self._value = tk.StringVar(value=value)
        self._entry = tk.Entry(master=self, textvariable=self._value,
                               bg=SUBFRAME_COLORS[0], relief=tk.FLAT,
                               highlightbackground=SUBFRAME_COLORS[0],
                               fg=VALUE_COLORS[1])
        self._entry.pack(fill=tk.X, side=tk.RIGHT)

    def get_value(self):
        """Return the value from the input."""
        return self._value.get()


class MultipleOptions(Input):
    """Multiple choice input."""

    def __init__(self, master, label, value, values):
        """Construct the multi input."""
        super(MultipleOptions, self).__init__(master, label)

        self._value = tk.StringVar(master=self)
        self._value.set(value)

        self._is_int = isinstance(value, int)

        self._entry = tk.OptionMenu(self, self._value, *values)
        self._entry.config(bg=SUBFRAME_COLORS[0], relief=tk.FLAT,
                           highlightbackground=SUBFRAME_COLORS[0],
                           fg=VALUE_COLORS[1])
        self._entry.pack(fill=tk.X, side=tk.LEFT)

    def get_value(self):
        """Return the value from the input."""
        if self._is_int:
            return int(self._value.get())
        else:
            return self._value.get()


class Slider(Input):
    """Slider int input style."""

    def __init__(self, master, label, value, min_val, max_val):
        """Construct the slider."""
        super(Slider, self).__init__(master, label)

        if value < min_val or value > max_val:
            raise Exception('Slider value exceedes limits!')
        else:
            self._value = tk.StringVar(value=value)

        self._entry = tk.Scale(master=self, from_=min_val, to=max_val,
                               orient=tk.HORIZONTAL)
        self._entry.config(bg=SUBFRAME_COLORS[0], relief=tk.FLAT,
                           highlightbackground=SUBFRAME_COLORS[0],
                           fg=VALUE_COLORS[1])

        self._entry.set(value)
        self._entry.pack(fill=tk.X, side=tk.LEFT)

    def get_value(self):
        """Return the value from the entry."""
        return int(self._entry.get())
