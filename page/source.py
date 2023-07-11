from typing import Any

from tkinter import END, W, E, N, S

from tk_up.managerWidgets import ManagerWidgets_up

from tk_up.widgets.frame import Frame_up
from tk_up.widgets.treeview import Treeview_up
from tk_up.widgets.button import Button_up, Toggle_Button_up

from tk_up.object.image import Wimage

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

class source(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    manager_class: ManagerWidgets_up

    def __init__(self, context: dict, manager_class: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.manager_class = manager_class

        self.tm: ThreadManager = self.ctx["tm"]
        self.langs: Lang = self.ctx["lib"][0]
        self.log: Logger = self.ctx["lib"][2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")

        self.frameButton = Frame_up(self)
        self.frameButton.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()

        self.l = Treeview_up(self, show="headings", resize_column=False)
        self.l.placePosSize(350, 300, 200, 200, anchor="center").show()

        test = ("test", "test2")

        self.l.addElement(values=test[0])
        self.l.setColumns(("Source",))

        self.add_button = Button_up(self.frameButton, command=self.addMenu, style="nobg.TButton", images=[
            Wimage(self.ctx["exe_path"]+"/img/add.png", (36, 36)),
            Wimage(self.ctx["exe_path"]+"/img/addSub.png", (36, 36)),
        ])
        self.add_button.gridPosSize(column=0, row=0).show()

        self.edit_button = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/edit.png", (36, 36))], command=self.editMenu, style="nobg.TButton")
        self.edit_button.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

        self.remove = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/delete.png", (36, 36))], command=self.delete, style="nobg.TButton")
        self.remove.gridPosSize(column=2, row=0, padx=5).show().disable()

        self.move_down = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/down.png", (36, 36))], command=self.treeView.moveDownSelectedElement, style="nobg.TButton")
        self.move_down.gridPosSize(column=3, row=0, padx=(25, 0)).show().disable()

        self.move_up = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/up.png", (36, 36))], command=self.treeView.moveUpSelectedElement, style="nobg.TButton")
        self.move_up.gridPosSize(column=4, row=0, padx=(0, 25)).show().disable()

        self.unselect_button = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/selectNone.png", (36, 36))], command=self.unselect, style="nobg.TButton")
        self.unselect_button.gridPosSize(column=5, row=0, padx=5).show().disable()

        self.onOffRule_button = Toggle_Button_up(self.frameButton, style="nobg.TButton")
        self.onOffRule_button.set_toggle_function(func1=self.onOffRule, func2=self.onOffRule)
        self.onOffRule_button.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.onOffRule_button.gridPosSize(column=6, row=0).show().disable()

    def showSelected(self, e):
        self.log.debug(self.l.getSelectedElement(), "SOURCE")

    # this function is call if you hide widget
    def disable(self) -> None:
        pass

    # this function is call if you show widget
    def enable(self) -> None:
        pass
    
    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None:
        pass