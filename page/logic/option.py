from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.option import option

def export_conf(self: "option"):
    try:
        if self.config.exportConfig():
            messagebox.showinfo("Export", "Config is exported")
    except Exception as e:
        self.log.error(e)

def import_conf(self: "option"):
    try:
        if self.config.importConfig():
            messagebox.showinfo("Import", "Config is imported")
    except Exception as e:
        self.log.error(e)

def fixLang(self: "option", event):
    lc = self.langs.getLocaleShort(self.combox_option_lang.get())
    self.config.CONFIG["lang"] = lc
    self.config.saveConfig()
    self.langs.setLang(lc)
    self.log.debug(f"lang : {self.langs.defaultLang}")
    self.event_generate("<<TK_UP.Update>>")
    self.tm.start("lang")

def delete_conf(self: "option"):

    try:
        if messagebox.askyesno("Delete Config", "Are you sure you want to delete the config ?"):
            self.config.delete()
            messagebox.showinfo("Delete Config", "The 'config.json' file has been deleted")
    except Exception as e:
        self.log.error(e)