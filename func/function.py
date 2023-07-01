from time import sleep
from tk_up.widgets.label import Label_up



def sendMessage(label: Label_up, color: str, message: str, time: int=7):
    label.config(text=message, foreground=color)
    sleep(time)
    label.config(text="")