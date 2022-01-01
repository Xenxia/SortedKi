from func.ui import Tk_up
from tkinter import Button

root = Tk_up(customTitleBar=True)

activecomp = {
    'titleBarTitle': True
}

root.configWindows()
root.configTitleBar(color="#25292e", active=activecomp)


close_button = Button(root, text="button")
close_button.pack()


root.run()