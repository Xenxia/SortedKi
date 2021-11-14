from tkinter import Button, Label, Text
from tkinter.constants import DISABLED, NORMAL

class Button_v(Button):

    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Button.__init__(self, master=master, cnf=cnf, **kw)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def conf_pos(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

class Label_v(Label):

    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Label.__init__(self, master=master, cnf=cnf, **kw)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def conf_pos(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

class Text_v(Text):

    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master=master, cnf=cnf, **kw)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0


    def conf_pos(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

