
from threading import Thread
from tkinter import E, W, S, N
from tk_up.widgets import Frame_up, Button_up, Terminal_ScrolledText_up, Separator_up
from tk_up.managerWidgets import ManagerWidgets_up
from func.logger import Logger
from func.langages import Lang_app

class menu_sort(Frame_up):

    parameters_list: list
    parameters_dict: dict
    manager_class: ManagerWidgets_up

    def __init__(self, parameters_list: list, parameters_dict: dict, manager_class: ManagerWidgets_up, master=None, kw={"width":0, "height":0}):
        self.parameters_list = parameters_list.copy()
        self.parameters_dict = parameters_dict
        self.manager_class = manager_class

        langs: Lang_app = parameters_list[0]
        log: Logger = parameters_list[2]

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        #command=lambda: Thread(target=sort).start()

        self.button_tree = Button_up(self, text=langs.lang['UI']['MAIN_MENU']['button_sort'], command=lambda: Thread(target=self.parameters_dict["sort_func"]).start())
        self.button_tree.placePosSize(350, 12, 86, 24, anchor="center").show()

        self.button_clear = Button_up(self, text=langs.lang['UI']['MAIN_MENU']['button_clear'])
        self.button_clear.placePosSize(350, 38, 86, 24, anchor="center").show()

        self.sep = Separator_up(self).placePosSize(0, 52, 700, 0).show()
        self.sep2 = Separator_up(self).placePosSize(0, 669, 700, 0).show()

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
        self.console1.placePosSize(0, 53, 700, 615).show()

    def disable(self):
        button: Button_up = self.parameters_list[3]
        button.disable()

    def enable(self):
        button: Button_up = self.parameters_list[3]
        button.enable()