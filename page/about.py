from typing import Any
import webbrowser, pyperclip
from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.button import Button_up
from tk_up.widgets.label import Label_up
from tk_up.managerWidgets import ManagerWidgets_up
from tkinter import E, W, S, N
import datetime
from Pylogger import Logger
from Pylang import Lang
from func.conf import Config_, PLATFORM_SYS

class about(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    wManager: ManagerWidgets_up

    def __init__(self, context: dict[str, Any], wManager: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.wManager = wManager

        self.langs: Lang = self.ctx["lib"][0]
        self.conf: Config_ = self.ctx["lib"][1]
        self.log: Logger = self.ctx["lib"][2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))


        # ==

        self.aboutLabel = Label_up(self, text=f"Developper : Xenxia\nOrganisation : Cheese-grinder\n\n© {datetime.date.today().year} Cheese-grinder")
        self.aboutLabel.placePosSize(350, 100, 250, 140, anchor="center").show()

        self.linkBtn = Button_up(self, text=f"Project Link : https://github.com/Xenxia/{self.ctx['app_name']}", command=lambda: webbrowser.open(f'https://github.com/Xenxia/{self.ctx["app_name"]}'), style="link.TButton")
        self.linkBtn.placePosSize(350, 200, 350, 24, anchor="center").show()

        self.linkBtn2 = Button_up(self, text=f"Create New Issues", command=lambda: webbrowser.open(f'https://github.com/Xenxia/{self.ctx["app_name"]}/issues/new/choose'))
        self.linkBtn2.placePosSize(350, 230, 150, 24, anchor="center").show()


        self.sysFrame = LabelFrame_up(self, text="Info System")
        self.sysFrame.placePosSize(350, 360, 310, 200, anchor="center").show()
        self.sysFrame.columnconfigure(0, weight=1)

        self.sysLabel = Label_up(self.sysFrame, text=" Error")
        self.sysLabel.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()

        self.button_return = Button_up(self, text="Copy sys info", command=lambda: pyperclip.copy(self.t))
        self.button_return.placePosSize(350, 490, 130, 24, anchor="center").show()

        self.button_return = Button_up(self, text=self.langs.t('UI.ABOUT.button_return'), command=lambda: wManager.showWidget("option"))
        self.button_return.placePosSize(350, 550, 120, 24, anchor="center").show()

    # this function is call if you hide widget
    def disable(self):
        pass

     # this function is call if you show widget
    def enable(self):
        systemInfo = [
            f"System Lang : {self.langs.getLocaleSys()}",
            f"System OS : {PLATFORM_SYS}",
            f"App version : {self.ctx['app_version']}",
            f"App last version : {self.ctx['app_last_version']}",
        ]

        self.t = ""
        for i in systemInfo:
            self.t = self.t + f" {i}\n"

        self.sysLabel.configure(text=self.t)
        self.sysLabel.update()

        