from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.option import option

def export_conf(self: "option"):
    try:
        if self.config.exportConfig():
            messagebox.showinfo(
                self.langs.t("UI.OPTION_MENU.box_confirm_export", 0),
                self.langs.t("UI.OPTION_MENU.box_confirm_export", 1)
            )
    except Exception as e:
        self.log.error(e)

def import_conf(self: "option"):
    try:
        if self.config.importConfig():
            messagebox.showinfo(
                self.langs.t("UI.OPTION_MENU.box_confirm_import", 0),
                self.langs.t("UI.OPTION_MENU.box_confirm_import", 1)
            )
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
        if messagebox.askyesno(
                self.langs.t("UI.OPTION_MENU.box_ask_delete", 0),
                self.langs.t("UI.OPTION_MENU.box_ask_delete", 1)
            ):
            self.config.delete()
            messagebox.showinfo(
                self.langs.t("UI.OPTION_MENU.box_confirm_delete", 0),
                self.langs.t("UI.OPTION_MENU.box_confirm_delete", 1)
            )
    except Exception as e:
        self.log.error(e)