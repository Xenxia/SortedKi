from os import execl
from tkinter import Button, Entry, Frame, Label, Text
from tkinter.constants import BOTH, BOTTOM, DISABLED, E, END, HORIZONTAL, LEFT, NO, NORMAL, RIGHT, TOP, VERTICAL, W, X, Y
from tkinter import ttk
from typing import Tuple

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

class Treeview_v(Frame):
    x: int
    y: int
    width: int
    height: int
    style: ttk.Style
    tree: ttk.Treeview
    scroll_v: ttk.Scrollbar
    scroll_h: ttk.Scrollbar

    def __init__(self, master=None, cnf={}, **kw):

        Frame.__init__(self, master=master, cnf=cnf, **kw)

        self.frameTreeview = Frame(self, bg="#202020", width=600, height=300)
        self.frameTreeview.grid(row=0, column=0, sticky=W)
        self.frameTreeview.propagate(False)

        self.frameButton = Frame(self, bg="#202020")
        self.frameButton.grid(row=1, column=0, sticky=W)

        self.frameBox = Frame(self, bg="#202020", width=600)
        self.frameBox.grid(row=2, column=0, sticky=W)
        self.frameBox.propagate(False)

        self.styleInit()

        nl = Label(self.frameBox, text="Profile Name ", bg="#202020", fg="#00ca00")
        nl.grid(row=0, column=0, sticky=W,)

        il = Label(self.frameBox, text="Folder ", bg="#202020", fg="#00ca00")
        il.grid(row=1, column=0, sticky=W)

        tl = Label(self.frameBox, text="Extention ", bg="#202020", fg="#00ca00")
        tl.grid(row=2, column=0, sticky=W)

        Unselect = Button_v(self.frameButton, text="Unselect", command=self.unselect, bg="#555555", fg="#00ca00", activebackground="#555555")
        Unselect.grid(column=5, row=0, padx=5)

        move_up = Button_v(self.frameButton, text="⬆", command=self.up, bg="#555555", fg="#00ca00", activebackground="#555555")
        move_up.grid(column=4, row=0)

        move_down = Button_v(self.frameButton, text="⬇", command=self.down, bg="#555555", fg="#00ca00", activebackground="#555555")
        move_down.grid(column=3, row=0)

        remove = Button_v(self.frameButton, text="Delete", command=self.remove, bg="#555555", fg="#00ca00", activebackground="#555555")
        remove.grid(column=2, row=0, padx=5)

        save = Button_v(self.frameButton, text="Save", command=self.save, bg="#555555", fg="#00ca00", activebackground="#555555")
        save.grid(column=1, row=0, padx=(5, 0))

        add = Button_v(self.frameButton, text="Add", command=self.add, bg="#555555", fg="#00ca00", activebackground="#555555")
        add.grid(column=0, row=0)

        self.name_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
        self.name_box.grid(row=0, column=1, sticky=W)

        self.id_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
        self.id_box.grid(row=1, column=1, sticky=W)

        self.topping_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
        self.topping_box.grid(row=2, column=1, sticky=W)

        self.scroll_v = ttk.Scrollbar(master=self.frameTreeview, orient=VERTICAL)
        self.scroll_v.pack(side=RIGHT, fill=Y)

        self.scroll_h = ttk.Scrollbar(master=self.frameTreeview, orient=HORIZONTAL)
        self.scroll_h.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(master=self.frameTreeview, yscrollcommand=self.scroll_v.set, xscrollcommand=self.scroll_h.set, selectmode="browse")
        self.tree.bind("<ButtonRelease-1>", self.selected)
        self.tree.pack(fill=Y, expand=True)

        self.scroll_v.config(command=self.tree.yview)
        self.scroll_h.config(command=self.tree.xview)

        self.tree['columns'] = ("empty")

    def styleInit(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                background="#000000",
                foreground="#ffffff",
                rowheight=25,
                fieldbackground="#000000",
                bd=1
                )

        self.style.configure("Vertical.TScrollbar",
                background="#323232",
                arrowcolor="#ffffff",
                bordercolor="#000000",
                troughcolor='#252526',
                foreground="#ff0000"
                )

        self.style.configure("Horizontal.TScrollbar",
                background="#323232",
                arrowcolor="#ffffff",
                bordercolor="#000000",
                troughcolor='#252526',
                foreground="#ff0000"
                )

        self.style.configure("Treeview.Heading", 
                background="black", 
                foreground="white"
                )

        self.style.map("Vertical.TScrollbar", background=[('pressed', '#229922')])
        self.style.map("Horizontal.TScrollbar", background=[('pressed', '#229922')])
        self.style.map('Treeview.Heading', background=[('selected', '#000000')])
        self.style.map('Treeview', background=[('selected', '#228B22')])

    def position(self, x: int, y: int, width: int = None, height: int = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def setColumns(self, columns: Tuple[str]):
        self.tree['columns'] = columns

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.heading("#0", text="")

        for col in columns:
            self.tree.column(col, anchor=W, minwidth=100)
            self.tree.heading(col, text=col, )

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

    # event
    def selected(self, event):
        self.select()

    def select(self):
        # Clear entry boxes
        self.name_box.delete(0, END)
        self.id_box.delete(0, END)
        self.topping_box.delete(0, END)

        # Grab record number
        try:
            selected = self.tree.selection()[0]
            values = self.tree.item(selected, 'values')

            # output to entry boxes
            self.name_box.insert(0, values[0])
            self.id_box.insert(0, values[1])
            self.topping_box.insert(0, values[2])

        except:
            print("not select")
        # Grab record values
        

    def remove(self):
        try:
            x = self.tree.selection()[0]
            self.tree.delete(x)
        except:
            print("not select")

    def add(self):

        name = self.name_box.get()
        id = self.id_box.get()
        topping = self.topping_box.get()

        if name!="" and id!="" and topping!="":
            self.tree.insert(parent='', index=END, text="", values=(self.name_box.get(), self.id_box.get(), self.topping_box.get()), tags=('evenrow',))
            self.unselect()
        else:
            print("box empty")

    def save(self):
        try:
            selected = self.tree.selection()[0]
            self.tree.item(selected, text="", values=(self.name_box.get(), self.id_box.get(), self.topping_box.get()))
            self.unselect()
        except:
            print("not select")

    def unselect(self):
        # Clear the boxes
        self.name_box.delete(0, END)
        self.id_box.delete(0, END)
        self.topping_box.delete(0, END)
        try:
            self.tree.selection_remove(self.tree.selection()[0])
        except:
            print("not select")

    def up(self):
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)-1)

    def down(self):
        rows = self.tree.selection()
        for row in reversed(rows):
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)+1)

class Frame_v(Frame):
    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master=master, cnf=cnf, **kw)
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

class Entry_v(Entry):
    x: int
    y: int
    width: int
    height: int

    def __init__(self, master=None, cnf={}, **kw):
        Entry.__init__(self, master=master, cnf=cnf, **kw)
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