from tkinter import END
from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.source import source


# Button logic =================================================================
def delete(self: "source"):
    self.listSource.removeSelectedItem()
    unselect(self)

def unselect(self: "source"):
    try:
        self.editSourceBtn.disable()
        self.removeSourceBtn.disable()
        self.unselectSourceBtn.disable()
        self.moveUpSourceBtn.disable()
        self.moveDownSourceBtn.disable()
        self.enableDisableSourceBtn.disable()
        self.listSource.tree.selection_remove(self.listSource.tree.selection()[0])
    except:
        self.log.debug("No Item selected")

def selected(self: "source", event):
    if self.listSource.getItemSelectedRow():

        item = self.listSource.getItemSelectedRow()
        if not "Disable" in item["tags"]:
            self.enableDisableSourceBtn.set_status(True, True)
        elif "Disable" in item["tags"]:
            self.enableDisableSourceBtn.set_status(False, True)

        if item["values"][0] == "Root":
            self.editSourceBtn.disable()
            self.removeSourceBtn.disable()
        else:
            self.editSourceBtn.enable()
            self.removeSourceBtn.enable()

        self.unselectSourceBtn.enable()
        self.moveUpSourceBtn.enable()
        self.moveDownSourceBtn.enable()
        self.enableDisableSourceBtn.enable()

def onOffSource(self: "source"):

    tags = self.listSource.getItemSelectedRow()["tags"]
    self.log.debug(tags)
    if not "Disable" in tags:
        self.listSource.editSelectedItem(tags="Disable")
    elif "Disable" in tags:
        self.listSource.editSelectedItem(tags="")
        # self.treeView.update()



#=================================================================
def addDataToList(self: "source"):
    self.listSource.removeAllItems()

    item: dict = self.config.CONFIG['sources']

    self.log.debug(item)

    for sourceName, sourceValue in item.items():

        self.log.debug(str(sourceName)+" : "+str(sourceValue))

        path: str = sourceValue["path"]

        tag = ""

        if sourceValue['disable']:
            tag = "Disable"

        self.log.debug(self.listSource.addItem(iid=sourceName, values=(sourceName, path), tags=tag))

def saveDataInList(self: "source"):

    self.config.CONFIG['sources'] = {}

    for _, d in self.listSource.getItems().items():

        key = d["values"][0]
        self.config.CONFIG['sources'][key] = {}

        path = d['values'][1]
        tags = d['tags']

        self.config.CONFIG['sources'][key]['path'] = path
        self.config.CONFIG['sources'][key]['disable'] = False

        if 'Disable' in tags:
            self.config.CONFIG['sources'][key]['disable'] = True


    self.config.saveConfig()

    self.wManager.showWidget("option")