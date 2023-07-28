from tkinter import W, E, N, S
from typing import Any

from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.button import Button_up, Toggle_Button_up
from tk_up.widgets.view import Treeview_up, Listview_up
from tk_up.widgets.separator import Separator_up
from tk_up.widgets.label import Label_up
from tk_up.widgets.toplevel import Toplevel_up
from tk_up.widgets.entry import Entry_up
from tk_up.managerWidgets import ManagerWidgets_up
from tk_up.enum import Scroll

from tk_up.object.image import Wimage

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from func.conf import Config_
from func.function import sendMessage

from page.logic.rules import *
from page.logic.rules_toplevel import *

class rules(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    wManager: ManagerWidgets_up

    def __init__(self, context: dict[str, Any], wManager: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.wManager = wManager

        self.tm: ThreadManager = self.ctx["tm"]
        self.langs: Lang = self.ctx["lib"][0]
        self.config: Config_ = self.ctx["lib"][1]
        self.log: Logger = self.ctx["lib"][2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        self.grid_propagate(False)

        self.frameButton = Frame_up(self)
        self.frameButton.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()

        self.frameBox = Frame_up(self, width=700)
        self.frameBox.gridPosSize(row=4, column=0, sticky=(E, W, S, N)).show()
        # self.frameBox.propagate(False)
        
        self.sep = Separator_up(self).gridPosSize(row=3, column=0, sticky=(E, W), pady=(2,0)).show()

        self.treeViewRules = Treeview_up(self, scroll=Scroll.ALL, child=True, editRow=True, width=700, height=400)
        self.treeViewRules.bind("<ButtonRelease-1>", lambda event: selected(self, event))
        self.treeViewRules.gridPosSize(row=2, column=0, sticky=(E, W, S, N)).show()
        self.treeViewRules.setColumns(
            columns=[
                self.langs.t('UI.EDIT_MENU_RULE.col_name_profil'),
                self.langs.t('UI.EDIT_MENU_RULE.col_folder'),
                self.langs.t('UI.EDIT_MENU_RULE.col_extention')
            ], 
            size=[150, 150, 300]
        )
        self.treeViewRules.setTags((
            {
            "name": "Disable",
            "fg": "#F70000",
            },
            {
            "name": "SysDisable",
            "bg": "#AA0000",
            },
        ))

        self.addItemBtn = Button_up(self.frameButton, command=lambda: addMenu(self), style="nobg.TButton", images=[
            Wimage(self.ctx["exe_path"]+"/img/add.png", (36, 36)),
            Wimage(self.ctx["exe_path"]+"/img/addSub.png", (36, 36)),
        ])
        self.addItemBtn.gridPosSize(column=0, row=0).show()

        self.editItemBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/edit.png", (36, 36))], command=lambda: editMenu(self), style="nobg.TButton")
        self.editItemBtn.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

        self.removeItemBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/delete.png", (36, 36))], command=lambda: delete(self), style="nobg.TButton")
        self.removeItemBtn.gridPosSize(column=2, row=0, padx=5).show().disable()

        self.moveDownItemBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/down.png", (36, 36))], command=self.treeViewRules.moveDownSelectedItem, style="nobg.TButton")
        self.moveDownItemBtn.gridPosSize(column=3, row=0, padx=(25, 0)).show().disable()

        self.moveUpItemBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/up.png", (36, 36))], command=self.treeViewRules.moveUpSelectedItem, style="nobg.TButton")
        self.moveUpItemBtn.gridPosSize(column=4, row=0, padx=(0, 25)).show().disable()

        self.unselectItemBtn = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/selectNone.png", (36, 36))], command=lambda: unselect(self), style="nobg.TButton")
        self.unselectItemBtn.gridPosSize(column=5, row=0, padx=5).show().disable()

        self.enableDisableRuleBtn = Toggle_Button_up(self.frameButton, style="nobg.TButton")
        self.enableDisableRuleBtn.set_toggle_function(func1=lambda: onOffRule(self), func2=lambda: onOffRule(self))
        self.enableDisableRuleBtn.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.enableDisableRuleBtn.gridPosSize(column=6, row=0).show().disable()


        notSortLabel = Label_up(self.frameBox, text=self.langs.t('UI.EDIT_MENU_RULE.label_not_sort'), anchor=W)
        notSortLabel.gridPosSize(row=0, column=0, pady=(20, 10), padx=(5, 10)).show()

        self.notSortEntry = Entry_up(self.frameBox, width=80)
        self.notSortEntry.grid(row=0, column=1, sticky=W, pady=(13, 0))

        unsortedLabel = Label_up(self.frameBox, text=self.langs.t('UI.EDIT_MENU_RULE.label_unsorted'), justify="right")
        unsortedLabel.gridPosSize(row=1, column=0, padx=(5, 10)).show()

        self.unsortedBtn = Toggle_Button_up(self.frameBox, style="nobg.TButton")
        self.unsortedBtn.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.unsortedBtn.gridPosSize(column=1, row=1, sticky=W).show()

        # self.back = Button_up(self.frameBox, text="back", width=10, command=lambda: self.manager_class.showWidget("menu_option"))
        # self.back.gridPosSize(column=0, row=2, padx=(5, 0), pady=(50, 0)).show()

        # return
        self.returnSaveFrame = LabelFrame_up(self, text="-")
        self.returnSaveFrame.placePosSize(350, 570, 120, 80, anchor="center").show()
        self.returnSaveFrame.columnconfigure(0, weight=1)
        # self.frame_return.rowconfigure(1, weight=1)
        # self.frame_return.rowconfigure(2, weight=1)
        # self.frame_return.grid_propagate(True)

        self.saveAndReturnBtn = Button_up(self.returnSaveFrame, text=self.langs.t('UI.EDIT_MENU_RULE.button_return_save'), command=lambda: saveDataInTree(self))
        self.saveAndReturnBtn.gridPosSize(column=0, row=1, sticky=(E, W), pady=(3,0), ipady=2).show()

        self.returnBtn = Button_up(self.returnSaveFrame, text=self.langs.t('UI.EDIT_MENU_RULE.button_return'), command=lambda: self.wManager.showWidget("option"))
        self.returnBtn.gridPosSize(column=0, row=2, sticky=(E, W), pady=(3,0), ipady=2).show()

        #### ==== TopLevel ====

        self.addOrEditToplevel = Toplevel_up(self.ctx["screenMain"]).configWindows(geometry="700x330+center", iconbitmap=f"{self.ctx['exe_path']}/img/icon.ico")
        self.addOrEditToplevel.config(background='#000000')
        self.addOrEditToplevel.resizable(0, 0)
        self.addOrEditToplevel.hide()

        #Labels
        nameProfileLabel = Label_up(self.addOrEditToplevel, text=self.langs.t('UI.EDIT_MENU_RULE.col_name_profil'))
        nameProfileLabel.gridPosSize(row=0, column=0, sticky="W", padx=(5,5)).show()

        pathFolderLabel = Label_up(self.addOrEditToplevel, text=self.langs.t('UI.EDIT_MENU_RULE.col_folder'))
        pathFolderLabel.gridPosSize(row=1, column=0, sticky="NW", padx=(5,5)).show()

        ruleLabel = Label_up(self.addOrEditToplevel, text=self.langs.t('UI.EDIT_MENU_RULE.col_extention'))
        ruleLabel.gridPosSize(row=2, column=0, sticky="NW", padx=(5,5), pady=(15,0)).show()

        #Entry boxes
        self.nameProfileEntry = Entry_up(self.addOrEditToplevel, width=80, takefocus=True)
        self.nameProfileEntry.gridPosSize(row=0, column=1, sticky=W, pady=(10, 10)).show()

        self.pathFolderEntry = Entry_up(self.addOrEditToplevel, width=80)
        self.pathFolderEntry.gridPosSize(row=1, column=1, sticky=W, pady=(0, 10)).show()

        # self.rule_box = Entry_up(self.addEditWindow, width=80)
        # self.rule_box.gridPosSize(row=2, column=1, sticky=W).show()

        self.listRuleFrame = Frame_up(self.addOrEditToplevel)

        self.listRule = Listview_up(self.listRuleFrame, scroll=Scroll.Y, selectmode="extended", editRow=True, width=350, height=200)
        self.listRule.setColumnsSize([150])
        self.listRule.gridPosSize(row=0, column=1, rowspan=15, sticky=W).show()

        self.addRuleBtn = Button_up(self.listRuleFrame, command=self.listRule.addEmptyRow, style="nobg.TButton", images=[
            Wimage(self.ctx["exe_path"]+"/img/add.png", (36, 36)),
        ])
        self.addRuleBtn.gridPosSize(column=0, row=0).show()

        self.removeRuleFromListBtn = Button_up(self.listRuleFrame, images=[Wimage(self.ctx["exe_path"]+"/img/delete.png", (36, 36))], command=self.listRule.removeSelectedItem, style="nobg.TButton")
        self.removeRuleFromListBtn.gridPosSize(column=0, row=1).show()


        self.listRuleFrame.gridPosSize(row=2, column=1, sticky=W, pady=(5,0)).show()

        footerBtnFrame = Frame_up(self.addOrEditToplevel)

        self.addOrEditBtn = Button_up(footerBtnFrame, width=15)
        self.addOrEditBtn.gridPosSize(row=0, column=0, padx=(0,3)).show()

        self.cancelBtn = Button_up(footerBtnFrame, width=15, text=self.langs.t('UI.EDIT_MENU_RULE.button_cancel'), command=self.addOrEditToplevel.hide)
        self.cancelBtn.gridPosSize(row=0, column=1).show()

        footerBtnFrame.gridPosSize(row=3, column=1, sticky=W, pady=(15,0)).show()

    # this function is call if you hide widget
    def disable(self):
        unselect(self)

        # this function is call if you show class
    def enable(self):
        self.grid_propagate(False)
        addDataToTree(self)
        # pass







