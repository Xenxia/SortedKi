from tkinter import Button, Label, Text
from tkinter.constants import DISABLED, END, NORMAL

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

    def position(self, x: int, y: int, width: int, height: int):
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

    def position(self, x: int, y: int, width: int, height: int):
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


    def position(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

class Terminal_v(Text):

    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master=master, cnf=cnf, **kw)
        self.bind("<Key>", lambda e: self.__ctrlEvent(e))
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0


    def position(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

    def __ctrlEvent(self, event) -> None:
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            return "break"

    def printTerminal(self, text: str, colored_text: str = 'none', color: str = '#FFFFFF') -> None:
        self.insert(END, text + "\n")
        self.see(END)
        self.tag_config(color, background="#000000", foreground=color)
        if color != 'none':
            if colored_text == '*':
                colored_text = text
            pos = '1.0'
            while True:
                idx = self.search(colored_text, pos, END)
                if not idx:
                    break
                pos = '{}+{}c'.format(idx, len(colored_text))
                self.tag_add(color, idx, pos)

    def clearTerminal(self) -> None:
        self.delete("1.0","end")
