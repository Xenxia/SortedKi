from time import sleep
from tk_up.widgets import Label_up




def sendMessage(label: Label_up, color: str, message: str, time: int=7):
    label.config(text=message, foreground=color)
    label.show()
    sleep(time)
    label.config(text="")
    label.hide()