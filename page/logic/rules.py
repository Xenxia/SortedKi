from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.rules import rules

def delete(self: "rules"):
    self.treeViewRules.removeSelectedItem()
    unselect(self)


def editUi(self: "rules"):

    for i in self.treeViewRules.tree.get_children():
        self.treeViewRules.tree.delete(i)

    for key in self.config.CONFIG['config_sort']:
        folder: str = self.config.CONFIG['config_sort'][key]['folder']
        rule: list = self.config.CONFIG['config_sort'][key]['ext']
        parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

        parent = parent if parent is not None else ''

        self.treeViewRules.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(rule)])

    self.unsortedBtn.set_default_status(self.config.CONFIG["unsorted"])

    for i in self.config.CONFIG["sorting_exception"]:
        self.listException.addItem(values=[i])

def unselect(self: "rules"):
    try:
        self.editItemBtn.disable()
        self.removeItemBtn.disable()
        self.unselectItemBtn.disable()
        self.moveUpItemBtn.disable()
        self.moveDownItemBtn.disable()
        self.enableDisableRuleBtn.disable()
        self.treeViewRules.tree.selection_remove(self.treeViewRules.tree.selection()[0])
        self.addItemBtn.set_image("add")
    except:
        self.log.debug("No Item selected", "edit_rules.unselect")

#------------------------------------------------------------------------

def selected(self: "rules", event):
    if self.treeViewRules.getItemSelectedRow():

        tags = self.treeViewRules.getItemSelectedRow()["tags"]
        if not "Disable" in tags:
            self.enableDisableRuleBtn.set_status(True, True)
        elif "Disable" in tags:
            self.enableDisableRuleBtn.set_status(False, True)


        self.editItemBtn.enable()
        self.removeItemBtn.enable()
        self.unselectItemBtn.enable()
        self.moveUpItemBtn.enable()
        self.moveDownItemBtn.enable()
        self.enableDisableRuleBtn.enable()
        self.addItemBtn.set_image("addSub")

def onOffRule(self: "rules"):

    tags = self.treeViewRules.getItemSelectedRow()["tags"]
    self.log.debug(tags, "onOffRule")
    if not "Disable" in tags:
        self.treeViewRules.editSelectedItem(tags="Disable")
    elif "Disable" in tags:
        self.treeViewRules.editSelectedItem(tags="")
        # self.treeView.update()



def saveDataInTree(self: "rules"):

    self.config.CONFIG['config_sort'] = {}

    for item in self.treeViewRules.getItems().items():
        key = ""
        fullPath = ""
        pathStatic = False

        self.config.CONFIG['config_sort'][item[0]] = {}
        key = item[0]

        value = item[1]['values']
        tags = item[1]['tags']

        self.config.CONFIG['config_sort'][key]['disable'] = False

        if 'Disable' in tags:
            self.config.CONFIG['config_sort'][key]['disable'] = True

        self.config.CONFIG['config_sort'][key]['parent'] = item[1]['parent']
        self.config.CONFIG['config_sort'][key]['folder'] = value[1]

        for index, parent in enumerate(self.treeViewRules.getParentsIID(key)):

            folder = self.treeViewRules.getItem(parent)["values"][1]

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
        self.config.CONFIG['config_sort'][key]['rule'] = value[2].split("|")
        self.config.CONFIG['config_sort'][key]['pathStatic'] = pathStatic

    self.config.CONFIG["unsorted"] = self.unsortedBtn.get_status()

    exception = []

    for _, i in self.listException.getItems().items():
        exception.append(i["values"][0])

    self.config.CONFIG["sorting_exception"] = exception
    

    self.config.saveConfig()

    self.wManager.showWidget("option")

def addDataToTree(self: "rules"):

    self.log.debug("ici")

    self.treeViewRules.removeAllItems()

    for key in self.config.CONFIG['config_sort']:
        folder: str = self.config.CONFIG['config_sort'][key]['folder']
        rule: list = self.config.CONFIG['config_sort'][key]['rule']
        parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

        tag = ""

        if self.config.CONFIG['config_sort'][key]['disable']:
            tag = "Disable"

        parent = parent if parent is not None else ''

        self.treeViewRules.addItem(parent=parent, iid=key, values=[key, folder, '|'.join(rule)], tags=tag)

    self.unsortedBtn.set_default_status(self.config.CONFIG["unsorted"])

    self.listException.removeAllItems()
    for i in self.config.CONFIG["sorting_exception"]:
        self.listException.addItem(values=[i])

