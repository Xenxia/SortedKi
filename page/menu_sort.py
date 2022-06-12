
from tkinter import E, W, S, N
from tk_up.widgets import Frame_up, Button_up, Terminal_ScrolledText_up
from tk_up.managerWidgets import ManagerWidgets_up
from func.logger import Logger
from func.langages import Lang_app

class menu_sort(Frame_up):

    parameters: list
    manager_class: ManagerWidgets_up

    def __init__(self, parameters: list, manager_class: ManagerWidgets_up, master=None, **kw):
        self.parameters = parameters
        self.manager_class = manager_class

        langs: Lang_app = parameters[0]
        log: Logger = parameters[2]

        Frame_up.__init__(self, master=master, **kw)
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        #command=lambda: Thread(target=sort).start()

        self.button_tree = Button_up(self, text=langs.lang['UI']['MAIN_MENU']['button_sort'])
        self.button_tree.placePosSize(350, 12, 80, 24, anchor="center").show()

        self.button_clear = Button_up(self, text=langs.lang['UI']['MAIN_MENU']['button_clear'])
        self.button_clear.placePosSize(350, 36, 80, 24, anchor="center").show()

        colorConsole = {
            "Green": ["", "#00ff00"],
            "Blue": ["", "#26abff"],
            "Orange": ["", "#ff7f00"],
            "Red": ["", "#ff0000"],
            "Purple": ["", "#ff0aff"],
            "Purple2": ["", "#743DFF"]
        }
        self.console1 = Terminal_ScrolledText_up(self, borderwidth=0)
        self.console1.configTag(colorConsole)
        self.console1.placePosSize(0, 48, 700, 620).show()