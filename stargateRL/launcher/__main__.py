"""The main launcher for changing the configurations."""

from Tkinter import Tk
from stargateRL.launcher import elements


root = Tk()
# GUI goes bellow this line

mf = elements.MainFrame(root)
mf.make_subframes(elements.SUBFRAMES_TITLES)

elements.IntegerInput(mf.subframes['RESOURCES'], 'tile size', 16)
elements.IntegerInput(mf.subframes['WINDOW'], 'width', 1440)
elements.IntegerInput(mf.subframes['WINDOW'], 'height', 900)
elements.BooleanInput(mf.subframes['WINDOW'], 'fullscreen', False)
elements.BooleanInput(mf.subframes['WINDOW'], 'resizable', False)
elements.BooleanInput(mf.subframes['WINDOW'], 'display mouse', False)

# GUI goes above this line
root.mainloop()
root.destroy()
