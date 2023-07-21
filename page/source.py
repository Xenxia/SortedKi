from typing import Any

from tkinter import END, W, E, N, S

from tk_up.managerWidgets import ManagerWidgets_up

from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.treeview import Treeview_up
from tk_up.widgets.button import Button_up, Toggle_Button_up

from tk_up.widgets import SCROLL_ALL

from tk_up.object.image import Wimage

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from func.conf import ConfigTree

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
        self.config: ConfigTree = self.ctx["lib"][1]


        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        self.grid_propagate(False)

        self.frameButton = Frame_up(self)
        self.frameButton.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()

        self.list = Treeview_up(self, scroll=SCROLL_ALL, show="headings", width=700, height=400)
        self.list.gridPosSize(row=1, column=0).show()
        self.list.bind("<ButtonRelease-1>", self.selected)
        self.list.setColumns(("Source Name", "Source Path"), size=[200, 250])
        self.list.setTags((
            {
            "name": "Disable",
            "fg": "#F70000",
            },
            {
            "name": "SysDisable",
            "bg": "#AA0000",
            },
        ))

        self.add_button = Button_up(self.frameButton, style="nobg.TButton", images=[
            Wimage(self.ctx["exe_path"]+"/img/add.png", (36, 36)),
        ])
        self.add_button.gridPosSize(column=0, row=0).show()

        self.edit_button = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/edit.png", (36, 36))], style="nobg.TButton")
        self.edit_button.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

        self.remove = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/delete.png", (36, 36))], command=self.delete, style="nobg.TButton")
        self.remove.gridPosSize(column=2, row=0, padx=5).show().disable()

        self.move_down = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/down.png", (36, 36))], command=self.list.moveDownSelectedElement, style="nobg.TButton")
        self.move_down.gridPosSize(column=3, row=0, padx=(25, 0)).show().disable()

        self.move_up = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/up.png", (36, 36))], command=self.list.moveUpSelectedElement, style="nobg.TButton")
        self.move_up.gridPosSize(column=4, row=0, padx=(0, 25)).show().disable()

        self.unselect_button = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/selectNone.png", (36, 36))], command=self.unselect, style="nobg.TButton")
        self.unselect_button.gridPosSize(column=5, row=0, padx=5).show().disable()

        self.onOffSource_button = Toggle_Button_up(self.frameButton, style="nobg.TButton")
        self.onOffSource_button.set_toggle_function(func1=self.onOffSource, func2=self.onOffSource)
        self.onOffSource_button.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.onOffSource_button.gridPosSize(column=6, row=0).show().disable()

        # return
        self.frame_return = LabelFrame_up(self, text="-")
        self.frame_return.placePosSize(350, 570, 120, 80, anchor="center").show()
        self.frame_return.columnconfigure(0, weight=1)

        self.button_saveAndReturn = Button_up(self.frame_return, text=self.langs.t('UI.EDIT_MENU.button_return_save'))
        self.button_saveAndReturn.gridPosSize(column=0, row=1, sticky=(E, W), pady=(3,0), ipady=2).show()

        self.button_return = Button_up(self.frame_return, text=self.langs.t('UI.EDIT_MENU.button_return'), command=lambda: self.manager_class.showWidget("option"))
        self.button_return.gridPosSize(column=0, row=2, sticky=(E, W), pady=(3,0), ipady=2).show()


    # Button logic =================================================================
    def delete(self):
        self.list.removeSelectedElement()
        self.unselect()

    def unselect(self):
        try:
            self.edit_button.disable()
            self.remove.disable()
            self.unselect_button.disable()
            self.move_up.disable()
            self.move_down.disable()
            self.onOffSource_button.disable()
            self.list.tree.selection_remove(self.list.tree.selection()[0])
            self.add_button.set_image("add")
        except:
            self.log.debug("No Item selected")

    def selected(self, event):
        if self.list.getItemSelectedRow():

            tags = self.list.getItemSelectedRow("tags")
            if not "Disable" in tags:
                self.onOffSource_button.set_status(True, True)
            elif "Disable" in tags:
                self.onOffSource_button.set_status(False, True)

            self.edit_button.enable()
            self.remove.enable()
            self.unselect_button.enable()
            self.move_up.enable()
            self.move_down.enable()
            self.onOffSource_button.enable()
            self.add_button.set_image("addSub")

    def onOffSource(self):

        tags = self.list.getItemSelectedRow("tags")
        self.log.debug(tags)
        if not "Disable" in tags:
            self.list.editSelectedElement(tags="Disable")
        elif "Disable" in tags:
            self.list.editSelectedElement(tags="")
            # self.treeView.update()

    

    #=================================================================
    def addDataToList(self):
        for i in self.list.tree.get_children():
            self.list.tree.delete(i)

        item: dict = self.config.CONFIG['source']

        self.log.debug(item)

        for sourceName, sourceValue in item.items():

            self.log.debug(str(sourceName)+" : "+str(sourceValue))

            path: str = sourceValue["path"]

            tag = ""

            if sourceValue['disable']:
                tag = "Disable"

            # self.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(rule)))
            self.log.debug(self.list.addElement(iid=END, values=(sourceName, path), tags=tag))

    # this function is call if you hide widget
    def disable(self) -> None:
        pass

    # this function is call if you show widget
    def enable(self):
        self.grid_propagate(False)
        self.addDataToList()
    
    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None:
        pass