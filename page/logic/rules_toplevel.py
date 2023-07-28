from tkinter import END
from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.rules import rules

from rules import unselect

#Toplevel menu ------------------------------------------------------------------------
def editMenu(self: "rules"):
    
    self.addOrEditToplevel.title(self.langs.t('UI.EDIT_MENU_RULE.title_edit'))

    self.addOrEditBtn.config(text=self.langs.t('UI.EDIT_MENU_RULE.button_apply'))

    self.nameProfileEntry.delete(0, END)
    self.pathFolderEntry.delete(0, END)
    self.listRule.removeAllItems()

    self.addOrEditBtn.config(command=lambda: edit(self))

    try:
        selected: list[str] = self.treeViewRules.getItemSelectedRow()["values"]
        # values = self.treeView.tree.item(selected, 'values')

        # output to entry boxes
        self.nameProfileEntry.insert(0, selected[0])
        self.pathFolderEntry.insert(0, selected[1])
        # self.rule_box.insert(0, selected[2])
        for v in selected[2].split("|"):
            self.listRule.addItem("", values=[v])
        

        self.addOrEditToplevel.show()

    except:
        self.log.debug("Not select", "editMenu")

def edit(self: "rules"):

    try:

        iid = self.treeViewRules.tree.selection()[0]

        rule = []

        for _, v in self.listRule.getItems().items():
            rule.append(v["values"][0])


        self.treeViewRules.editItem(iid, values=[self.nameProfileEntry.get(), self.pathFolderEntry.get(), "|".join(rule)])
        self.addOrEditToplevel.hide()
    except ValueError as e:
        self.log.debug("error : "+e)

def addMenu(self: "rules"):
    if self.treeViewRules.isSelect():
        self.addOrEditToplevel.title(self.langs.t('UI.EDIT_MENU_RULE.title_add_sub'))
    else:
        self.addOrEditToplevel.title(self.langs.t('UI.EDIT_MENU_RULE.title_add'))

    self.addOrEditBtn.config(text=self.langs.t('UI.EDIT_MENU_RULE.button_add'))

    self.nameProfileEntry.delete(0, END)
    self.pathFolderEntry.delete(0, END)
    self.listRule.removeAllItems()

    self.addOrEditBtn.config(command=lambda: add(self))

    self.addOrEditToplevel.show()

def add(self: "rules"):
    profile_name = self.nameProfileEntry.get()
    folder = self.pathFolderEntry.get()
    
    rule = []

    for _, v in self.listRule.getItems().items():
        rule.append(v["values"][0])

    sellect = ""

    try:
        sellect = self.treeViewRules.tree.selection()[0]
    except:
        self.log.debug("No select")

    if profile_name!="" and folder!="":
        try:
            self.treeViewRules.tree.insert(parent=sellect, index=END, iid=profile_name, text=profile_name, values=(folder, "|".join(rule)), tags=('evenrow',))
            unselect(self)
            self.addOrEditToplevel.hide()
            self.log.debug("ok")

        except ValueError as e:
            self.log.debug("error : "+e)

    else:
        self.tm.start("requireProfileNameFolder")
        self.log.debug("Profile name and Folder is required")