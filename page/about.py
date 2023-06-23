import webbrowser
from tk_up.widgets import Frame_up, Label_up, Button_up
from tk_up.managerWidgets import ManagerWidgets_up
from tkinter import E, W, S, N, CENTER
import datetime
from Pylogger import Logger
from Pylang import Lang

class about(Frame_up):

    # DONT REMOVE THIS
    parameters_list: list
    parameters_dict: dict
    manager_class: ManagerWidgets_up

    def __init__(self, parameters_list: list, parameters_dict: dict, manager_class: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.parameters_list = parameters_list.copy()
        self.parameters_dict = parameters_dict.copy()
        self.manager_class = manager_class

        self.langs: Lang = parameters_list[0]
        self.log: Logger = parameters_list[2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))


        # ==

        self.about_text = Label_up(self, text=f"Developper : Xenxia\nOrganisation : Cheese-grinder\n\n© {datetime.date.today().year} Cheese-grinder")
        self.about_text.placePosSize(350, 100, 250, 140, anchor="center").show()

        self.button_link = Button_up(self, text=f"Project Link : https://github.com/Xenxia/{self.parameters_dict['app_name']}", command=lambda: webbrowser.open(f'https://github.com/Xenxia/{self.parameters_dict["app_name"]}'), style="link.TButton")
        self.button_link.placePosSize(350, 200, 350, 24, anchor="center").show()

        self.button_return = Button_up(self, text=self.langs.t('UI.ABOUT.button_return'), command=lambda: manager_class.showWidget("menu_option"))
        self.button_return.placePosSize(350, 550, 120, 24, anchor="center").show()


    # this function is call if you hide widget
    def disable(self):
        pass

     # this function is call if you show widget
    def enable(self):
        pass