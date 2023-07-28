from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.option import option

def export_conf(self: "option"):
    try:
        self.config.exportConfig()
        self.tm.start("confExport")
    except:
        print('export')

def import_conf(self: "option"):
    try:
        self.config.importConfig()
        self.tm.start("confImport")
    except:
        print('import')

def fixLang(self: "option", event):
    lc = self.langs.getLocaleShort(self.combox_option_lang.get())
    self.config.CONFIG["lang"] = lc
    self.config.saveConfig()
    self.langs.setLang(lc)
    self.log.debug(f"lang : {self.langs.defaultLang}")
    self.event_generate("<<TK_UP.Update>>")
    self.tm.start("lang")

def delete_conf(self: "option"):

    self.config.delete()
    self.tm.start("confDelete")