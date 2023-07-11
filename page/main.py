from typing import Any
from PyThreadUp import ThreadManager
from tkinter import E, W, S, N
from tk_up.widgets.frame import Frame_up
from tk_up.widgets.button import Button_up
from tk_up.widgets.text import Terminal_ScrolledText_up
from tk_up.widgets.separator import Separator_up

from tk_up.object.image import Wimage

from tk_up.managerWidgets import ManagerWidgets_up

from Pylogger import Logger
from Pylang import Lang

class main(Frame_up):

     # DONT REMOVE THIS
    ctx: dict[str, Any]
    manager_class: ManagerWidgets_up

    def __init__(self, context: dict[str, Any], manager_class: ManagerWidgets_up, master=None, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.manager_class = manager_class

        tm: ThreadManager = self.ctx["tm"]
        langs: Lang = self.ctx["lib"][0]
        log: Logger = self.ctx["lib"][2]

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        #command=lambda: Thread(target=sort).start()
        
        self.console1 = Terminal_ScrolledText_up(self, borderwidth=0)

        self.button_tree = Button_up(self, image=Wimage(self.ctx["exe_path"]+"/img/start.png", (46, 46)), command=lambda: tm.start("sort"), style="nobg.TButton")
        self.button_tree.placePosSize(350, 25, 48, 48, anchor="center").show()

        self.button_clear = Button_up(self, image=Wimage(self.ctx["exe_path"]+"/img/clear.png", (20, 20)), command=self.console1.clearTerminal, style="nobg.TButton")
        self.button_clear.placePosSize(690, 43, 24, 24, anchor="center").show()

        self.sep = Separator_up(self).placePosSize(0, 52, 700, 0).show()
        self.sep2 = Separator_up(self).placePosSize(0, 669, 700, 0).show()

        colorConsole = {
            "Green": {
                "background": "",
                "foreground": "#00ff00"},
            "Blue": {
                "background": "",
                "foreground": "#26abff"},
            "Orange": {
                "background": "",
                "foreground": "#ff7f00"},
            "Red": {
                "background": "",
                "foreground": "#ff0000"},
            "Purple": {
                "background": "",
                "foreground": "#ff0aff"},
            "Purple2": {
                "background": "",
                "foreground": "#743DFF"},
            "Bold": {
                "font" : ("Consolas", 11, "bold")
            }
        }
        self.console1.configTag(colorConsole)
        self.console1.placePosSize(0, 53, 700, 615).show()

    def disable(self):
        button: Button_up = self.ctx["btn_option"]
        button.disable()

    def enable(self):
        button: Button_up = self.ctx["btn_option"]
        button.enable()