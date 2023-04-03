
from PyThreadUp import ThreadManager
from tkinter import E, W, S, N
from tk_up.widgets import Frame_up, Button_up, Terminal_ScrolledText_up, Separator_up
from tk_up.managerWidgets import ManagerWidgets_up
from Pylogger import Logger
from Pylang import Lang

class menu_sort(Frame_up):

    parameters_list: list
    parameters_dict: dict
    manager_class: ManagerWidgets_up

    def __init__(self, parameters_list: list, parameters_dict: dict, manager_class: ManagerWidgets_up, master=None, kw={"width":0, "height":0}):
        self.parameters_list = parameters_list.copy()
        self.parameters_dict = parameters_dict
        self.manager_class = manager_class

        tm: ThreadManager = self.parameters_dict["tm"]
        langs: Lang = parameters_list[0]
        log: Logger = parameters_list[2]

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        #command=lambda: Thread(target=sort).start()
        
        self.console1 = Terminal_ScrolledText_up(self, borderwidth=0)

        self.button_tree = Button_up(self, text=langs.t('UI.MAIN_MENU.button_sort'), command=lambda: tm.start("sort"))
        self.button_tree.placePosSize(350, 12, 86, 24, anchor="center").show()

        self.button_clear = Button_up(self, text=langs.t('UI.MAIN_MENU.button_clear'), command=self.console1.clearTerminal)
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
        self.console1.configTag(colorConsole)
        self.console1.placePosSize(0, 53, 700, 615).show()

    def disable(self):
        button: Button_up = self.parameters_list[3]
        button.disable()

    def enable(self):
        button: Button_up = self.parameters_list[3]
        button.enable()