import tkinter, platform, re as regex
from tkinter import IntVar, StringVar, Tk, ttk
from typing import Any, Literal, Tuple
from tkinter import Button, Canvas, Entry, Frame, Grid, Label, Pack, Place, Text, Widget, Toplevel
from tkinter.constants import BOTH, BOTTOM, DISABLED, END, HORIZONTAL, LEFT, NO, NORMAL, RIGHT, VERTICAL, W, X, Y, YES

PLATFORM_SYS = platform.system()

if PLATFORM_SYS == "Windows":
    from ctypes import windll

SCROLL_X: str = "scroll_x"
SCROLL_Y: str = "scroll_y"
SCROLL_ALL: str = "scroll_all"

def setAppWindow(mainWindow, windows = None): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True)
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic

    hwnd: Any

    if windows is None:
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    else:
        hwnd = windll.user32.GetParent(windows.winfo_id())

    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    if windows is None:
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    else:
        windows.wm_withdraw()
        windows.wm_deiconify()

#CLASS

class ScrolledText(Text):

    def __init__(self, master=None, **kw):

        self.frame = Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)

class Tk_up(Tk, Frame):

    titleBarComponent: list
    funcRunAfter: list = []
    customTitleBar: bool
    root: Tk

    # Title bar info
    activeComp: dict = {
        'titleBarTitle': True,
        'closeButton': True,
        'expandButton': True,
        'minimizeButton': True,
    }
    title: str
    geometry: str

    # Size screen
    rootHeigth: int
    rootWidth: int

    # Component
    __titleBar: Frame

    def __init__(self, customTitleBar:bool=False) -> None:
        self.customTitleBar=customTitleBar

        if customTitleBar:
            self.root = Tk()
            self.rootHeigth = self.root.winfo_screenheight()
            self.rootWidth = self.root.winfo_screenwidth()
            self.root.minimized = False
            self.root.maximized = False
            self.root.overrideredirect(True)
            self.__titleBar = Frame(self.root, relief='raised', bd=0, highlightthickness=0)
            self.titleBarTitle = Label_up(self.__titleBar, bd=0, fg='white', font=("helvetica", 10), highlightthickness=0)
            self.closeButton = Button_up(self.__titleBar, text=' 🗙 ', command=self.root.destroy, font=("calibri", 11), bd=0, fg='white', highlightthickness=0)
            self.expandButton = Button_up(self.__titleBar, text=' 🗖 ', bd=0, fg='white', font=("calibri", 11), highlightthickness=0)
            self.minimizeButton = Button_up(self.__titleBar, text=' 🗕 ', bd=0, fg='white', font=("calibri", 11), highlightthickness=0)
            self.titleBarComponent = [
                self.__titleBar,
                self.titleBarTitle,
                self.minimizeButton,
                self.closeButton,
                self.expandButton
            ]
            if PLATFORM_SYS == "Windows":
                self.runAfterMainloopStarted(lambda: setAppWindow(self.root))
            Frame.__init__(self, master=self.root ,highlightthickness=0)
        else:
            Tk.__init__(self)
            self.rootWidth = self.winfo_screenwidth()
            self.rootHeigth = self.winfo_screenheight()

    def __getPos(self, event):

        if self.root.maximized == False:
            
            xwin = self.root.winfo_x()
            ywin = self.root.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event): # runs when window is dragged
                self.root.config(cursor="fleur")
                self.root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


            def release_window(event): # runs when window is released
                self.root.config(cursor="arrow")
                
            self.__titleBar.bind('<B1-Motion>', move_window)
            self.__titleBar.bind('<ButtonRelease-1>', release_window)
            # title_bar_title.bind('<B1-Motion>', move_window)
            # title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            self.expandButton.config(text=" 🗖 ")
            self.root.maximized = not self.root.maximized

    def configWindows(self, title:str="Tk_Up", geometry:str="500x500", iconbitmap:str=None):

        if regex.findall(r"\+center", geometry) != []:
            gSizeW, gSizeH = geometry.split("+", 1)[0].split("x", 1)
            rootH = round((self.rootHeigth/2)-(int(gSizeH)/2))
            rootW = round((self.rootWidth/2)-(int(gSizeW)/2))
            geometry = f'{gSizeW}x{gSizeH}+{rootW}+{rootH}'
        
        if self.customTitleBar:
            self.titleBarTitle.configure(text=title)
        
            self.root.title(title)
            self.root.geometry(geometry)

            if iconbitmap is not None:
                self.root.iconbitmap(iconbitmap)

        else:
            self.title(title)
            self.geometry(geometry)
            if iconbitmap is not None:
                self.iconbitmap(iconbitmap)

    def configTitleBar(self, color:str="#ffffff", active:dict[str, bool]=None, c_closeButton:dict=None):

        if self.customTitleBar:

            if active is not None:
                self.activeComp.update(active)

            for comp in self.titleBarComponent:
                comp.configure(bg=color)

    def runAfterMainloopStarted(self, func: Any):
        self.funcRunAfter.append(func)

    def run(self):
        if self.customTitleBar:
            self.__titleBar.bind('<Button-1>', self.__getPos)
            self.__titleBar.pack(side="top", fill=X)
            if self.activeComp['titleBarTitle']: self.titleBarTitle.pack(side=LEFT, padx=(10, 0))
            if self.activeComp['closeButton']: self.closeButton.pack(side=RIGHT)
            if self.activeComp['expandButton']: self.expandButton.pack(side=RIGHT)
            if self.activeComp['minimizeButton']: self.minimizeButton.pack(side=RIGHT)
            self.pack(expand=1, fill=BOTH)
            for func in self.funcRunAfter:
                self.root.after(10, func)
            self.root.mainloop()
        else:
            if self.funcRunAfter == []:
                for func in self.funcRunAfter:
                    self.after(10, func)
            self.mainloop()

class Widget_up(Widget):

    #Place
    x: int
    y: int
    width: int
    height: int

    #Grid
    row: int
    column: int
    sticky: str
    pady: tuple
    padx: tuple

    #Sys
    sysShowHide: str

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def placePosSize(self, x: int, y: int, width: int, height: int = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.sysShowHide = "place"

        return self

    def gridPosSize(self, row: int, column: int, pady: tuple = None ,padx: tuple = None ,sticky: str = None):
        self.row = row
        self.column = column
        self.sticky = sticky
        self.pady = pady
        self.padx = padx

        self.sysShowHide = "grid"

        return self

    def show(self):

        if self.sysShowHide == "place":
            self.place(x=self.x, y=self.y, width=self.width, height=self.height)
        elif self.sysShowHide == "grid":
            self.grid(row=self.row, column=self.column, sticky=self.sticky, pady=self.pady, padx=self.padx)
        else:
            raise ValueError

        return self

    def hide(self):
        if self.sysShowHide == "place":
            self.place_forget()
        elif self.sysShowHide == "grid":
            self.grid_forget()
        else:
            raise ValueError

        return self


class Toplevel_up(Toplevel, Frame):

    __disableTitleBar: bool

    # Component
    __titleBar: Frame
    top: Toplevel

    def __init__(self, master=None, disableTitleBar:bool=False, cnf={}, **kw):

        self.__disableTitleBar = disableTitleBar

        
        Toplevel.__init__(self, master=master, cnf=cnf, **kw)
        self.protocol("WM_DELETE_WINDOW", self.hide)

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

class Button_up(Button, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Button.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

class Toggle_Button_up(Button_up):

    text: Tuple = ("ON", "OFF")
    color: Tuple = ("#00FF00", "#FF0000")
    status: bool

    def __init__(self, master=None, cnf={}, **kw):
        Button_up.__init__(self, master=master, cnf=cnf, **kw, command=self.toggle)
        self.status = True
        self.reload()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def reload(self):
        if self.status:
            self.config(text=self.text[0])
            self.config(fg=self.color[0])
            self.status = True
        else:
            self.config(text=self.text[1])
            self.config(fg=self.color[1])
            self.status = False

    def custom_toggle(self, text: Tuple = None, color: Tuple = None):
        if text is not None: self.text = text
        if color is not None: self.color = color
        self.reload()

    def set_default_status(self, status: bool):
        self.status = status
        self.reload()

    def get_status(self) -> bool:
        return self.status

    def toggle(self):
    
        if self.config('text')[-1] == self.text[0]:
            self.config(text=self.text[1])
            self.config(fg=self.color[1])
            self.status = False
        else:
            self.config(text=self.text[0])
            self.config(fg=self.color[0])
            self.status = True

class Label_up(Label, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Label.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Text_up(Text, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class ScrolledText_up(ScrolledText, Widget_up):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Terminal_ScrolledText_up(ScrolledText, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        self.bind("<Key>", lambda e: self.__ctrlEvent(e))

    def __ctrlEvent(self, event) -> None:
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            return "break"

    def configTag(self, tag: dict):
        for key, value in tag.items():
            self.tag_configure(key, background=value[0], foreground=value[1])

    def printTerminal(self, *texts, color: list = None) -> None:
        for index, text in enumerate(texts):
            if text == texts[-1]:
                self.insert(END, text+ "\n", color[index])
            else:
                self.insert(END, text, color[index])
        self.see(END)

    def clearTerminal(self) -> None:
        self.delete("1.0","end")

class Treeview_up(Frame, Widget_up):
    __count: int = 10
    __iid: bool
    __child: bool
    tree: ttk.Treeview
    scroll_y: ttk.Scrollbar
    scroll_x: ttk.Scrollbar

    def __init__(self, master=None, scroll:str=None, iid:bool=False, child:bool=False, show="tree", cnf={}, **kw):

        Frame.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

        self.propagate(False)

        self.__child=child
        self.__iid=iid

        self.tree = ttk.Treeview(
            master=self,
            show=show,
            selectmode="browse",
            height=(kw["height"] if "height" in kw else None)
        )

        if scroll != None:
            self.scroll_y = ttk.Scrollbar(master=self, orient=VERTICAL)
            self.scroll_y.pack(side=RIGHT, fill=Y)

            self.scroll_x = ttk.Scrollbar(master=self, orient=HORIZONTAL)
            self.scroll_x.pack(side=BOTTOM, fill=X)

            if scroll == SCROLL_X:
                self.scroll_x.config(command=self.tree.xview)
                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.scroll_y.destroy()

            if scroll == SCROLL_Y:
                self.scroll_y.config(command=self.tree.yview)
                self.tree.configure(yscrollcommand=self.scroll_y.set)
                self.scroll_x.destroy()

            if scroll == SCROLL_ALL:
                self.scroll_x.config(command=self.tree.xview)
                self.scroll_y.config(command=self.tree.yview)

                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.pack(fill=BOTH, expand=True)

        self.tree['columns'] = ("empty")

    def __popItem(self, dict:dict, position=0):

        key = list(dict.keys())[position]
        value = list(dict.values())[position]

        del dict[key]

        return (key, value), dict

    def __getSubChildren(self, tree, item=""):
        children: list = []
        list_children = tree.get_children(item)
        for child in list_children:
            children.append(child)
            children += self.__getSubChildren(tree, child)
        return children

    def bind(self, sequence:str|None= None, func=None, add:bool|Literal['', '+']|None=None) -> None:
        self.tree.bind(sequence=sequence, func=func, add=add)

    def addElements(self, data:dict=None) -> bool:

        temp: dict = {}

        while True:
            
            if len(data) == 0:
                data = temp
                temp = {}
            
            if (len(data) + len(temp)) == 0:
                return True

            while len(data) != 0:
                
                child, data = self.__popItem(data)

                print(child)

                if child[1]["parent"] not in data:
                    
                    iid: str = child[0]
                    parent: str = str(child[1]["parent"]) if child[1]["parent"] is not None else ""
                    
                    # Try Key values
                    try:
                        values: list | Tuple = child[1]["values"]
                    except KeyError:
                        print("values key")
                    # Try Key text
                    try:
                        text: str = child[1]["text"]
                    except KeyError:
                        text = ""

                    # Try Key image
                    try: 
                        image: Any = child[1]["image"] 
                    except KeyError: 
                        image = ""

                    # Try Key open
                    try:
                        open: bool = child[1]["open"]
                    except KeyError:
                        open = False

                    # Try Key tags
                    try:
                        tags: str = child[1]["tags"]
                    except KeyError:
                        tags = ""

                    if self.__child:
                        text = values.pop(0)

                    try:
                        self.tree.insert(
                                parent=parent, 
                                index=END,
                                iid=iid,
                                text=text, 
                                values=values, 
                                tags=tags, 
                                image=image, 
                                open=open
                            )
                    except tkinter.TclError:
                        return False

                    self.__count += 1
                else:
                    temp[child[0]] = child[1]

    def addElement(self, parent:str="", index:int|Literal['end']=END, iid:str=None, id:str="", text:str="", image="", values:list=[], open:bool=False, tags:str|list[str]|Tuple[str, ...]="") -> bool:
        if iid is None:
            iid = self.__count

        if self.__iid and iid is None:
            iid=values[0]

        if self.__child:
            text=values.pop(0)

        try:
            self.tree.insert(parent=parent, index=index, iid=iid, text=text, image=image, values=values, open=open, tags=tags)
            self.__count += 1
        except tkinter.TclError as error:
            return error
        return True

    def removeOneElement(self):
        item = self.tree.selection()[0]
        self.tree.delete(item)

    def removeAllElement(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    def removeSelectedElement(self):
        item = self.tree.selection()[0]
        self.tree.delete(item)

    def editSelectedElement(self, text:str="", image="", values:list|Literal['']="", open:bool=False, tags:str|list[str]|tuple[str, ...]=""):
        item = self.tree.focus()
        self.tree.item(item, text=text, image=image, values=values, open=open, tags=tags)

    def editElement(self, item:str, text:str="", image="", values:list|Literal['']="", open:bool=False, tags:str|list[str]|tuple[str, ...]="") -> None:
        self.tree.item(item, text=text, image=image, values=values, open=open, tags=tags)

    def getItemSelectedElemnt(self, option:str='values') -> Any:
        item = self.tree.focus()

        if self.__child and option == "values":
            listValues: list = []
            listValues.append(self.tree.item(item, "text"))
            for value in self.tree.item(item, "values"):
                listValues.append(value)
            return listValues

        return self.tree.item(item, option)

    def getSelectedElement(self) -> tuple:
        return self.tree.selection()

    def getAllChildren(self) -> dict:
        childs_list = self.__getSubChildren(self.tree)

        children_dict = {}

        for iid in childs_list:

            temp_dict = {}

            item = self.tree.item(iid)

            temp_dict["values"] = item["values"]
            temp_dict["text"] = item["text"]
            temp_dict["image"] = item["image"]
            temp_dict["open"] = item["open"]
            temp_dict["tags"] = item["tags"]
            temp_dict["parent"] = None

            parentIID = self.tree.parent(iid)

            if parentIID != "":
                temp_dict["parent"] = parentIID
            
            children_dict[iid] = (temp_dict)
        
        return children_dict

    def getAllParentItem(self, iidParent: str) -> list[str]:

        parentList = []

        while iidParent != '':
            parentList.append(iidParent)
            iidParent = self.tree.parent(iidParent)
        return parentList

    def getItem(self, iid: str) -> tuple | str:
        return self.tree.item(iid)

    def setColumns(self, columns: list[str], size: list[int] = None) -> None:

        if self.__child:
            firstColumn = columns.pop(0)
            firstColumnSize = size.pop(0)
            self.tree['columns'] = columns
            self.tree.column("#0", width=firstColumnSize, stretch=NO)
            self.tree.heading("#0", text=firstColumn)
        else:
            self.tree['columns'] = columns
            self.tree.column("#0", width=0, stretch=NO)
            self.tree.heading("#0", text="")

        end = columns[-1]

        for index, col in enumerate(columns):
            width = 100
            stch = NO

            if size is not None and len(columns) == len(size):
                width = size[index]

            if end == col:
                stch = YES

            self.tree.column(col, anchor=W, width=width, stretch=stch)
            self.tree.heading(col, text=col)

    def moveUpSelectedElement(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)-1)

    def moveDownSelectedElement(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)+1)

class Frame_up(Frame, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Entry_up(Entry, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Entry.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Canvas_up(Canvas, Widget_up):


    def __init__(self, master=None, cnf={}, **kw) -> None:

        Canvas.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class OptionMenu_up(ttk.Combobox, Widget_up):

    def __init__(self, master=None, style=None, type: str="str", default: int=None, list: Tuple | list=None, **kw) -> None:

        type_var: StringVar | IntVar

        if type == "str":
            type_var = StringVar()
        elif type == "int":
            type_var = IntVar()

        ttk.Combobox.__init__(self, master, values=list ,textvariable=type_var, state="readonly", **kw)
        Widget_up.__init__(self)

