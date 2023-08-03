from tkinter import END, messagebox
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

    nameProfile = self.nameProfileEntry.get()
    pathProfile = self.pathFolderEntry.get()

    if nameProfile == "":
        messagebox.showerror("Profile Name", "Profile name is require")
        self.log.error("Profile name is require")
        self.addOrEditToplevel.focus_force()
        return
    
    if pathProfile == "":
        messagebox.showerror("Profile Path", "Profile path is require")
        self.log.error("Profile path is require")
        self.addOrEditToplevel.focus_force()
        return

    try:

        iid = self.treeViewRules.tree.selection()[0]

        rule = []

        for _, v in self.listRule.getItems().items():
            rule.append(v["values"][0])


        self.treeViewRules.editItem(iid, values=[nameProfile, pathProfile, "|".join(rule)])
        self.addOrEditToplevel.hide()
    except ValueError as e:
        self.log.error("error : "+e)

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
    nameProfile = self.nameProfileEntry.get()
    pathProfile = self.pathFolderEntry.get()

    if nameProfile == "":
        messagebox.showerror("Profile Name", "Profile name is require")
        self.log.error("Profile name is require")
        self.addOrEditToplevel.focus_force()
        return
    
    if pathProfile == "":
        messagebox.showerror("Profile Path", "Profile path is require")
        self.log.error("Profile path is require")
        self.addOrEditToplevel.focus_force()
        return
    
    rule = []

    for _, v in self.listRule.getItems().items():
        rule.append(v["values"][0])

    sellect = ""

    try:
        sellect = self.treeViewRules.tree.selection()[0]
    except:
        self.log.debug("No select")

    try:
        self.treeViewRules.addItem(parent=sellect, iid=nameProfile, values=[nameProfile, pathProfile, "|".join(rule)], tags=('evenrow',))
        unselect(self)
        self.addOrEditToplevel.hide()
        self.log.debug("ok")

    except Exception as e:
        self.log.error("error : "+e)
