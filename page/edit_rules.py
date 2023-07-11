from tkinter import END, W, E, N, S
from typing import Any

from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.button import Button_up, Toggle_Button_up
from tk_up.widgets.treeview import Treeview_up
from tk_up.widgets.separator import Separator_up
from tk_up.widgets.label import Label_up
from tk_up.widgets.toplevel import Toplevel_up
from tk_up.widgets.entry import Entry_up
from tk_up.managerWidgets import ManagerWidgets_up
from tk_up.widgets import SCROLL_ALL

from tk_up.object.image import Wimage

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from PIL import Image, ImageTk

from func.conf import ConfigTree
from func.function import sendMessage

class edit_rules(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    manager_class: ManagerWidgets_up

    def __init__(self, context: dict[str, Any], manager_class: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.manager_class = manager_class

        self.tm: ThreadManager = self.ctx["tm"]
        self.langs: Lang = self.ctx["lib"][0]
        self.config: ConfigTree = self.ctx["lib"][1]
        self.log: Logger = self.ctx["lib"][2]

        temp = Image.open(self.ctx["exe_path"]+"/img/addSub.png")
        temp = temp.resize((36, 36), Image.LANCZOS)
        self.addSubImage = ImageTk.PhotoImage(temp, size=(36, 36))

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

        self.treeView = Treeview_up(self, scroll=SCROLL_ALL, iid=True, child=True, show="tree headings", width=700, height=400)
        self.treeView.bind("<ButtonRelease-1>", self.selected)
        self.treeView.gridPosSize(row=2, column=0, sticky=(E, W, S, N)).show()
        self.treeView.setColumns(
            columns=[
                self.langs.t('UI.EDIT_MENU.col_name_profil'),
                self.langs.t('UI.EDIT_MENU.col_folder'),
                self.langs.t('UI.EDIT_MENU.col_extention')
            ], 
            size=[150, 150, 300]
        )
        self.treeView.setTags((
            {
            "name": "Disable",
            "fg": "#F70000",
            },
            {
            "name": "SysDisable",
            "bg": "#AA0000",
            },
        ))

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
        self.move_down.gridPosSize(column=3, row=0, padx=(20, 0)).show().disable()

        self.move_up = Button_up(self.frameButton, images=[Wimage(self.ctx["exe_path"]+"/img/up.png", (36, 36))], command=self.treeView.moveUpSelectedElement, style="nobg.TButton")
        self.move_up.gridPosSize(column=4, row=0, padx=(0, 20)).show().disable()

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


        d1 = Label_up(self.frameBox, text=self.langs.t('UI.EDIT_MENU.label_not_sort'), anchor=W)
        d1.gridPosSize(row=0, column=0, pady=(20, 10), padx=(5, 10)).show()

        self.doNotSort_box = Entry_up(self.frameBox, width=80)
        self.doNotSort_box.grid(row=0, column=1, sticky=W, pady=(13, 0))

        u1 = Label_up(self.frameBox, text=self.langs.t('UI.EDIT_MENU.label_unsorted'), justify="right")
        u1.gridPosSize(row=1, column=0, padx=(5, 10)).show()

        self.toggle_b = Toggle_Button_up(self.frameBox, style="nobg.TButton")
        self.toggle_b.custom_toggle(
            image=(
                (self.ctx["exe_path"]+"/img/on.png", (36, 36)),
                (self.ctx["exe_path"]+"/img/off.png", (36, 36))
            )
        )
        self.toggle_b.gridPosSize(column=1, row=1, sticky=W).show()

        # self.back = Button_up(self.frameBox, text="back", width=10, command=lambda: self.manager_class.showWidget("menu_option"))
        # self.back.gridPosSize(column=0, row=2, padx=(5, 0), pady=(50, 0)).show()

        # return
        self.frame_return = LabelFrame_up(self, text="-")
        self.frame_return.placePosSize(350, 570, 120, 80, anchor="center").show()
        self.frame_return.columnconfigure(0, weight=1)
        # self.frame_return.rowconfigure(1, weight=1)
        # self.frame_return.rowconfigure(2, weight=1)
        # self.frame_return.grid_propagate(True)

        self.button_saveAndReturn = Button_up(self.frame_return, text=self.langs.t('UI.EDIT_MENU.button_return_save'), command=self.saveDataInTree)
        self.button_saveAndReturn.gridPosSize(column=0, row=1, sticky=(E, W), pady=(3,0), ipady=2).show()

        self.button_return = Button_up(self.frame_return, text=self.langs.t('UI.EDIT_MENU.button_return'), command=lambda: self.manager_class.showWidget("option"))
        self.button_return.gridPosSize(column=0, row=2, sticky=(E, W), pady=(3,0), ipady=2).show()

        self.label_error_edit = Label_up(self.frameBox, text="")
        self.label_error_edit.gridPosSize(column=0, row=3, padx=(5, 0), pady=(50, 0)).show()

        # TopLevel

        self.addEditWindow = Toplevel_up(self.ctx["screenMain"]).configWindows(geometry="700x95+center", iconbitmap=f"{self.ctx['exe_path']}/img/icon.ico")
        self.addEditWindow.config(background='#000000')
        self.addEditWindow.resizable(0, 0)
        self.addEditWindow.hide()

        #Labels
        nl = Label_up(self.addEditWindow, text=self.langs.t('UI.EDIT_MENU.col_name_profil'))
        nl.gridPosSize(row=0, column=0, sticky=W, padx=(5,5)).show()

        il = Label_up(self.addEditWindow, text=self.langs.t('UI.EDIT_MENU.col_folder'))
        il.gridPosSize(row=1, column=0, sticky=W, padx=(5,5)).show()

        tl = Label_up(self.addEditWindow, text=self.langs.t('UI.EDIT_MENU.col_extention'))
        tl.gridPosSize(row=2, column=0, sticky=W, padx=(5,5)).show()

        #Entry boxes
        self.profile_box = Entry_up(self.addEditWindow, width=80, takefocus=True)
        self.profile_box.gridPosSize(row=0, column=1, sticky=W).show()

        self.folder_box = Entry_up(self.addEditWindow, width=80)
        self.folder_box.gridPosSize(row=1, column=1, sticky=W).show()

        self.rule_box = Entry_up(self.addEditWindow, width=80)
        self.rule_box.gridPosSize(row=2, column=1, sticky=W).show()

        buttonF = Frame_up(self.addEditWindow)

        self.addOrEdit = Button_up(buttonF)
        self.addOrEdit.gridPosSize(row=0, column=0, padx=(0,3)).show()

        self.cancel = Button_up(buttonF, text=self.langs.t('UI.EDIT_MENU.button_cancel'), command=self.addEditWindow.hide)
        self.cancel.gridPosSize(row=0, column=1).show()

        buttonF.gridPosSize(row=3, column=1, sticky=W, pady=(5,0)).show()

        self.label_error_addEditWindow = Label_up(self.addEditWindow, text="")
        self.label_error_addEditWindow.placePosSize(x=200, y=63, width=300, height=32)

        self.tm.thread("noItemSelectError", target=lambda: sendMessage(self.label_error_addEditWindow, "#ff3030", f"no items selected"))
        self.tm.thread("profilNameExist", target=sendMessage)
        self.tm.thread("requireProfileNameFolder", target=lambda: sendMessage(self.label_error_addEditWindow, "#ff3030", f"Profile name and Folder is required"))

    def editUi(self):

        for i in self.treeView.tree.get_children():
            self.treeView.tree.delete(i)

        for key in self.config.CONFIG['config_sort']:
            folder: str = self.config.CONFIG['config_sort'][key]['folder']
            rule: list = self.config.CONFIG['config_sort'][key]['ext']
            parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

            parent = parent if parent is not None else ''

            self.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(rule)])

        self.toggle_b.set_default_status(self.config.CONFIG["unsorted"])
        doNotSort = "|".join(self.config.CONFIG["doNotSort"])
        if not doNotSort == "":
            self.doNotSort_box.delete(0, END)
            self.doNotSort_box.insert(0, doNotSort)

        # self.show()

    def delete(self):
        self.treeView.removeSelectedElement()
        self.unselect()

    def unselect(self):
        try:
            self.edit_button.disable()
            self.remove.disable()
            self.unselect_button.disable()
            self.move_up.disable()
            self.move_down.disable()
            self.onOffRule_button.disable()
            self.treeView.tree.selection_remove(self.treeView.tree.selection()[0])
            self.add_button.set_image("add")
        except:
            self.log.debug("No Item selected", "edit_rules.unselect")

#Toplevel menu ------------------------------------------------------------------------
    def editMenu(self):
        
        self.addEditWindow.title(self.langs.t('UI.EDIT_MENU.title_edit'))

        self.addOrEdit.config(text=self.langs.t('UI.EDIT_MENU.button_apply'))

        self.profile_box.delete(0, END)
        self.folder_box.delete(0, END)
        self.rule_box.delete(0, END)

        self.addOrEdit.config(command=self.edit)

        try:
            selected = self.treeView.getItemSelectedElement()
            # values = self.treeView.tree.item(selected, 'values')

            # output to entry boxes
            self.profile_box.insert(0, selected[0])
            self.folder_box.insert(0, selected[1])
            self.rule_box.insert(0, selected[2])
            

            self.addEditWindow.show()

        except:
            self.log.debug("Not select", "editMenu")

    def edit(self):
        try:
            selected = self.treeView.tree.selection()[0]
            self.treeView.tree.item(selected, text=self.profile_box.get(), values=(self.folder_box.get(), self.rule_box.get()))
            self.addEditWindow.hide()
        except:
            self.tm.start("noItemSelectError")

    def addMenu(self):
        if self.treeView.isSelect():
            self.addEditWindow.title("Add Sub Rule")
        else:
            self.addEditWindow.title(self.langs.t('UI.EDIT_MENU.title_add'))

        self.addOrEdit.config(text=self.langs.t('UI.EDIT_MENU.button_add'))

        self.profile_box.delete(0, END)
        self.folder_box.delete(0, END)
        self.rule_box.delete(0, END)

        self.addOrEdit.config(command=self.add)

        self.addEditWindow.show()

    def add(self):
        profile_name = self.profile_box.get()
        folder = self.folder_box.get()
        rule = self.rule_box.get()

        sellect = ""

        try:
            sellect = self.treeView.tree.selection()[0]
        except:
            self.log.debug("No select")

        if profile_name!="" and folder!="":
            try:
                self.treeView.tree.insert(parent=sellect, index=END, iid=profile_name, text=profile_name, values=(folder, rule), tags=('evenrow',))
                self.unselect()
                self.addEditWindow.hide()
            except:
                self.tm.set_args("profilNameExist", (self.label_error_addEditWindow, "#ff3030", f"The profile {profile_name} already exists")).start("profilNameExist")

        else:
            self.tm.start("requireProfileNameFolder")
            self.log.debug("Profile name and Folder is required")
#------------------------------------------------------------------------

    def selected(self, event):
        if self.treeView.getSelectedElement():

            tags = self.treeView.getItemSelectedElement("tags")
            if not "Disable" in tags:
                self.onOffRule_button.set_status(True, True)
            elif "Disable" in tags:
                self.onOffRule_button.set_status(False, True)


            self.edit_button.enable()
            self.remove.enable()
            self.unselect_button.enable()
            self.move_up.enable()
            self.move_down.enable()
            self.onOffRule_button.enable()
            self.add_button.set_image("addSub")

    def onOffRule(self):

        tags = self.treeView.getItemSelectedElement("tags")
        self.log.debug(tags, "onOffRule")
        if not "Disable" in tags:
            self.treeView.editSelectedElement(tags="Disable")
        elif "Disable" in tags:
            self.treeView.editSelectedElement(tags="")
            # self.treeView.update()



    def saveDataInTree(self):

        self.config.CONFIG['config_sort'] = {}

        for iid in self.treeView.getAllChildren().items():
            key = ""
            fullPath = ""
            pathStatic = False

            self.config.CONFIG['config_sort'][iid[0]] = {}
            key = iid[0]

            value = iid[1]['values']
            tags = iid[1]['tags']

            self.config.CONFIG['config_sort'][key]['disable'] = False

            if 'Disable' in tags:
                self.config.CONFIG['config_sort'][key]['disable'] = True

            self.config.CONFIG['config_sort'][key]['parent'] = iid[1]['parent']
            self.config.CONFIG['config_sort'][key]['folder'] = value[0]

            for index, parent in enumerate(self.treeView.getAllParentItem(key)):

                folder = self.treeView.getItem(parent)["values"][0]

                self.log.debug(f"p : {parent}, i : {index}, f : {folder}")

                if folder[0] == "/" or folder[1] == ":":
                    fullPath = folder + fullPath
                    pathStatic = True
                    break

                if index != 0:
                    fullPath = f"{folder}/{fullPath}"
                else:
                    fullPath = f"{folder}"

            self.log.debug(fullPath)


            # else:
                # for index, parent in enumerate(self.treeView.getAllParentItem(key)[::-1]):#

                #     folder = self.treeView.getItem(parent)["values"][0]

                #     if index != 0:
                #         fullPath += f"/{folder}"
                #     else:
                #         fullPath += f"{folder}"

            self.config.CONFIG['config_sort'][key]['fullPath'] = fullPath
            self.config.CONFIG['config_sort'][key]['rule'] = value[1].split("|")
            self.config.CONFIG['config_sort'][key]['pathStatic'] = pathStatic

        self.config.CONFIG["unsorted"] = self.toggle_b.get_status()
        doNotSort2 = self.doNotSort_box.get()
        if not doNotSort2 == "":
            self.config.CONFIG["doNotSort"] = doNotSort2.split("|")
        else:
            self.config.CONFIG["doNotSort"] = []

        self.config.saveConfig()

        self.manager_class.showWidget("option")

    def addDataToTree(self):
        for i in self.treeView.tree.get_children():
            self.treeView.tree.delete(i)

        for key in self.config.CONFIG['config_sort']:
            folder: str = self.config.CONFIG['config_sort'][key]['folder']
            rule: list = self.config.CONFIG['config_sort'][key]['rule']
            parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

            tag = ""

            if self.config.CONFIG['config_sort'][key]['disable']:
                tag = "Disable"

            parent = parent if parent is not None else ''

            # self.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(rule)))
            self.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(rule)], tags=tag)

        self.toggle_b.set_default_status(self.config.CONFIG["unsorted"])
        doNotSort = "|".join(self.config.CONFIG["doNotSort"])
        if not doNotSort == "":
            self.doNotSort_box.delete(0, END)
            self.doNotSort_box.insert(0, doNotSort)

    # this function is call if you hide widget
    def disable(self):
        self.unselect()

        # pass

     # this function is call if you show class
    def enable(self):
        self.grid_propagate(False)
        self.addDataToTree()
        # pass