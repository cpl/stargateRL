"""The main launcher for changing the configurations."""

from Tkinter import Tk
from stargateRL.launcher import elements


root = Tk()
# GUI goes bellow this line

mf = elements.MainFrame(root)
mf.make_subframes(elements.SUBFRAMES_TITLES)

elements.IntegerInput(mf._subframes['RESOURCES'], 'tile size', 16)
elements.IntegerInput(mf._subframes['WINDOW'], 'width', 1440)
elements.IntegerInput(mf._subframes['WINDOW'], 'height', 900)
elements.BooleanInput(mf._subframes['WINDOW'], 'fullscreen', False)
elements.BooleanInput(mf._subframes['WINDOW'], 'resizable', False)
elements.BooleanInput(mf._subframes['WINDOW'], 'display mouse', False)

# GUI goes above this line
root.mainloop()
root.destroy()
