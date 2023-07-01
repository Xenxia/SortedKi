from typing import Any
import webbrowser
from tk_up.widgets.frame import Frame_up
from tk_up.widgets.button import Button_up
from tk_up.widgets.label import Label_up
from tk_up.managerWidgets import ManagerWidgets_up
from tkinter import E, W, S, N
import datetime
from Pylogger import Logger
from Pylang import Lang

class about(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    manager_class: ManagerWidgets_up

    def __init__(self, context: dict[str, Any], manager_class: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.manager_class = manager_class

        self.langs: Lang = self.ctx["lib"][0]
        self.log: Logger = self.ctx["lib"][2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))


        # ==

        self.about_text = Label_up(self, text=f"Developper : Xenxia\nOrganisation : Cheese-grinder\n\n© {datetime.date.today().year} Cheese-grinder")
        self.about_text.placePosSize(350, 100, 250, 140, anchor="center").show()

        self.button_link = Button_up(self, text=f"Project Link : https://github.com/Xenxia/{self.ctx['app_name']}", command=lambda: webbrowser.open(f'https://github.com/Xenxia/{self.parameters_dict["app_name"]}'), style="link.TButton")
        self.button_link.placePosSize(350, 200, 350, 24, anchor="center").show()

        self.button_return = Button_up(self, text=self.langs.t('UI.ABOUT.button_return'), command=lambda: manager_class.showWidget("option"))
        self.button_return.placePosSize(350, 550, 120, 24, anchor="center").show()


    # this function is call if you hide widget
    def disable(self):
        pass

     # this function is call if you show widget
    def enable(self):
        pass