from typing import Any

from tkinter import END, W, E, N, S

from tk_up.managerWidgets import ManagerWidgets_up

from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.view import Treeview_up
from tk_up.widgets.button import Button_up, Toggle_Button_up
from tk_up.widgets.label import Label_up
from tk_up.widgets.entry import Entry_up
from tk_up.widgets.toplevel import Toplevel_up

from tk_up.enum import Scroll

from tk_up.object.image import Wimage

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from func.conf import Config_

from page.logic.source import *
from page.logic.source_toplevel import *

class source(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    wManager: ManagerWidgets_up

    def __init__(self, context: dict, wManager: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.wManager = wManager

        self.tm: ThreadManager = self.ctx["tm"]
        self.langs: Lang = self.ctx["lib"][0]
        self.log: Logger = self.ctx["lib"][2]
        self.config: Config_ = self.ctx["lib"][1]


        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        self.grid_propagate(False)

        self.frameButton = Frame_up(self)
        self.frameButton.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()

        self.listSource = Treeview_up(self, scroll=Scroll.Y, width=700, height=400)
        self.listSource.gridPosSize(row=1, column=0).show()
        self.listSource.bind("<ButtonRelease-1>", lambda e: selected(self, e))
        self.listSource.setColumns((
            self.langs.t('UI.EDIT_MENU_SOURCE.col_name_source'),
            self.langs.t('UI.EDIT_MENU_SOURCE.col_path')
        ), size=[200, 250])
        self.listSource.setTags((
            {
            "name": "Disable",
            "fg": "#F70000",
            },
            {
            "name": "SysDisable",
            "bg": "#AA0000",
            },
        ))

        self.addSourceBtn = Button_up(self.frameButton, style="nobg.TButton", command=lambda: addMenu(self), images=[
            Wimage(self.ctx["exe_path"]+"/img/add.png", (36, 36)),
        ])
        self.addSourceBtn.gridPosSize(column=0, row=0).show()

        self.editSourceBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/edit.png", (36, 36))], command=lambda: editMenu(self), style="nobg.TButton")
        self.editSourceBtn.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

        self.removeSourceBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/delete.png", (36, 36))], command=lambda: delete(self), style="nobg.TButton")
        self.removeSourceBtn.gridPosSize(column=2, row=0, padx=5).show().disable()

        self.moveDownSourceBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/down.png", (36, 36))], command=self.listSource.moveDownSelectedItem, style="nobg.TButton")
        self.moveDownSourceBtn.gridPosSize(column=3, row=0, padx=(25, 0)).show().disable()

        self.moveUpSourceBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/up.png", (36, 36))], command=self.listSource.moveUpSelectedItem, style="nobg.TButton")
        self.moveUpSourceBtn.gridPosSize(column=4, row=0, padx=(0, 25)).show().disable()

        self.unselectSourceBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/selectNone.png", (36, 36))], command=lambda: unselect(self), style="nobg.TButton")
        self.unselectSourceBtn.gridPosSize(column=5, row=0, padx=5).show().disable()

        self.enableDisableSourceBtn = Toggle_Button_up(self.frameButton, style="nobg.TButton")
        self.enableDisableSourceBtn.set_toggle_function(func1=lambda: onOffSource(self), func2=lambda: onOffSource(self))
        self.enableDisableSourceBtn.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.enableDisableSourceBtn.gridPosSize(column=6, row=0).show().disable()

        # return
        self.saveReturnFrame = LabelFrame_up(self, text="-")
        self.saveReturnFrame.placePosSize(350, 570, 120, 80, anchor="center").show()
        self.saveReturnFrame.columnconfigure(0, weight=1)

        self.saveAndReturnBtn = Button_up(self.saveReturnFrame, text=self.langs.t('UI.EDIT_MENU_SOURCE.button_return_save'), command=lambda: saveDataInList(self))
        self.saveAndReturnBtn.gridPosSize(column=0, row=1, sticky=(E, W), pady=(3,0), ipady=2).show()

        self.returnBtn = Button_up(self.saveReturnFrame, text=self.langs.t('UI.EDIT_MENU_SOURCE.button_return'), command=lambda: self.wManager.showWidget("option"))
        self.returnBtn.gridPosSize(column=0, row=2, sticky=(E, W), pady=(3,0), ipady=2).show()

        #### ==== TopLevel ====

        self.addOrEditSourceToplevel = Toplevel_up(self.ctx["screenMain"]).configWindows(geometry="700x130+center", iconbitmap=f"{self.ctx['exe_path']}/img/icon.ico")
        self.addOrEditSourceToplevel.config(background='#000000')
        self.addOrEditSourceToplevel.resizable(0, 0)
        self.addOrEditSourceToplevel.grid_propagate(False)
        self.addOrEditSourceToplevel.columnconfigure(0, minsize=155)
        self.addOrEditSourceToplevel.columnconfigure(1, minsize=500)
        self.addOrEditSourceToplevel.hide()
        

        #Labels
        nameSourceLabel = Label_up(self.addOrEditSourceToplevel, text=self.langs.t('UI.EDIT_MENU_SOURCE.col_name_source'))
        nameSourceLabel.gridPosSize(row=0, column=0, sticky="W", padx=(5,5)).show()

        pathFolderSourceLabel = Label_up(self.addOrEditSourceToplevel, text=self.langs.t('UI.EDIT_MENU_SOURCE.col_path'))
        pathFolderSourceLabel.gridPosSize(row=1, column=0, sticky="NW", padx=(5,5), pady=(6, 0)).show()

        #Entry boxes
        self.nameSourceEntry = Entry_up(self.addOrEditSourceToplevel, takefocus=True)
        self.nameSourceEntry.gridPosSize(row=0, column=1, columnspan=2, sticky="EW", pady=(10, 10)).show()

        self.pathFolderSourceEntry = Entry_up(self.addOrEditSourceToplevel)
        self.pathFolderSourceEntry.gridPosSize(row=1, column=1, sticky="EW", pady=(0, 10)).show()

        #button
        self.folderSourceBtn = Button_up(self.addOrEditSourceToplevel, image=Wimage(self.ctx["exe_path"]+"/img/browseFolder.png", (28, 28)), style="nobg.TButton", command=lambda: getFolder(self))
        self.folderSourceBtn.gridPosSize(row=1, column=2, sticky=W, pady=(0, 10), padx=(5, 0)).show()


        # ApplyCancel
        footerBtnFrame = Frame_up(self.addOrEditSourceToplevel)

        self.addOrEditBtn = Button_up(footerBtnFrame, width=15)
        self.addOrEditBtn.gridPosSize(row=0, column=0, padx=(0,3)).show()

        self.cancelBtn = Button_up(footerBtnFrame, width=15, text=self.langs.t('UI.EDIT_MENU_SOURCE.button_cancel'), command=self.addOrEditSourceToplevel.hide)
        self.cancelBtn.gridPosSize(row=0, column=1).show()

        footerBtnFrame.gridPosSize(row=3, column=1, sticky=W, pady=(15,0)).show()

    # this function is call if you hide widget
    def disable(self) -> None:
        unselect(self)

    # this function is call if you show widget
    def enable(self):
        self.grid_propagate(False)
        addDataToList(self)
    
    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None:
        pass