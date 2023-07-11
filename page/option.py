from tkinter import E, W, S, N, CENTER
from typing import Any

from tk_up.widgets.frame import Frame_up, LabelFrame_up
from tk_up.widgets.label import Label_up
from tk_up.widgets.button import Button_up
from tk_up.widgets.separator import Separator_up
from tk_up.widgets.optionmenu import OptionMenu_up

from tk_up.managerWidgets import ManagerWidgets_up

from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from func.conf import ConfigTree
from func.function import sendMessage

class option(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    manager_class: ManagerWidgets_up

    #parameters

    log: Logger
    config: ConfigTree
    langs: Lang

    def __init__(self, context: dict[str, Any], manager_class: ManagerWidgets_up, master=None, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.manager_class = manager_class

        self.tm: ThreadManager = self.ctx["tm"]

        self.langs: Lang = self.ctx["lib"][0]
        self.config: ConfigTree = self.ctx["lib"][1]
        self.log: Logger = self.ctx["lib"][2]

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))

        # self.log.debug(self.event_info(), "option_event")
        #command=lambda: Thread(target=sort).start()
    
        self.label_settings = Label_up(self, text=self.langs.t('UI.OPTION_MENU.settings'), wraplength=320, justify=CENTER, anchor="center")
        self.label_settings.placePosSize(350, 40, 150, 64, anchor="center").show()

        self.sep = Separator_up(self).placePosSize(350, 52, 500, 0, anchor=CENTER).show()

        ### Settings

        # Rule
        self.frame_rules = LabelFrame_up(self, text=self.langs.t('UI.OPTION_MENU.frame_rules'))
        self.frame_rules.placePosSize(190, 102, 120, 50, anchor="center").show()
        self.frame_rules.columnconfigure(0, weight=1)
        self.frame_rules.rowconfigure(3, weight=1)

        self.button_edit_rules = Button_up(self.frame_rules, text=self.langs.t('UI.OPTION_MENU.button_edit'), command=lambda: self.manager_class.showWidget("edit_rules"))
        self.button_edit_rules.gridPosSize(row=2, column=0, sticky=(E, W, S, N), pady=(3,0)).show()

        #Source
        self.frame_source = LabelFrame_up(self, text=self.langs.t('UI.OPTION_MENU.frame_source'))
        self.frame_source.placePosSize(510, 102, 120, 50, anchor="center").show()
        self.frame_source.columnconfigure(0, weight=1)
        self.frame_source.rowconfigure(3, weight=1)

        self.button_edit_source = Button_up(self.frame_source, text=self.langs.t('UI.OPTION_MENU.button_edit'), command=lambda: self.manager_class.showWidget("source"))
        self.button_edit_source.gridPosSize(row=2, column=0, sticky=(E, W, S, N), pady=(3,0)).show()

        #=======

        self.button_export = Button_up(self, text=self.langs.t('UI.OPTION_MENU.button_export'), command=self.export_conf)
        self.button_export.placePosSize(350, 75, 120, 24, anchor="center").show()

        self.button_import = Button_up(self, text=self.langs.t('UI.OPTION_MENU.button_import'), command=self.import_conf)
        self.button_import.placePosSize(350, 105, 120, 24, anchor="center").show()

        self.button_delete = Button_up(self, text=self.langs.t('UI.OPTION_MENU.button_delete_conf'), style="fgred.TButton")
        self.button_delete.placePosSize(350, 148, 120, 48, anchor="center").show()

        self.sep = Separator_up(self).placePosSize(350, 187, 500, 0, anchor=CENTER).show()

        # Warning
        self.frame_function_warning = LabelFrame_up(self, text="Warning")
        self.frame_function_warning.placePosSize(350, 260, 120, 120, anchor="center").show()
        self.frame_function_warning.columnconfigure(0, weight=1)
        self.frame_function_warning.rowconfigure(0, weight=1)
        self.frame_function_warning.rowconfigure(1, weight=1)

        self.button_sortedToRoot = Button_up(self.frame_function_warning, text=self.langs.t('UI.OPTION_MENU.button_sorted_root'), style="fgred.TButton")
        self.button_sortedToRoot.gridPosSize(row=0, column=0, sticky=(E, W, S, N), pady=(5,0)).show()
        self.button_unsortedToRoot = Button_up(self.frame_function_warning, text=self.langs.t('UI.OPTION_MENU.button_unsorted_root'), style="fgred.TButton")
        self.button_unsortedToRoot.gridPosSize(row=1, column=0, sticky=(E, W, S, N), pady=(5,10)).show()

        # Lang
        self.frame_lang = LabelFrame_up(self, text="lang")
        self.frame_lang.placePosSize(350, 365, 120, 51, anchor="center").show()
        self.frame_lang.columnconfigure(0, weight=1)
        # self.frame_lang.rowconfigure(3, weight=1)

        self.combox_option_lang = OptionMenu_up(self.frame_lang, default=0, list=self.langs.getLocalesLong(), justify='center')
        self.combox_option_lang.current(self.langs.getIndexDefaultLang())
        self.combox_option_lang.bind("<<ComboboxSelected>>", self.fixLang)
        self.combox_option_lang.gridPosSize(row=0, column=0, sticky=(E, W, S, N), pady=(5,0)).show()

        # Other
        self.button_return = Button_up(self, text=self.langs.t('UI.OPTION_MENU.button_return'), command=lambda: manager_class.showWidget("main"))
        self.button_return.placePosSize(350, 550, 120, 24, anchor="center").show()

        self.button_about = Button_up(self, text=self.langs.t('UI.ABOUT.button_about'), command=lambda: manager_class.showWidget("about"))
        self.button_about.placePosSize(350, 577, 120, 24, anchor="center").show()

        self.label_error_option = Label_up(self, text="", wraplength=320, justify=CENTER, anchor="center")
        self.label_error_option.placePosSize(350, 620, 320, 64, anchor="center").show()

        self.tm.thread("confExport", target=lambda: sendMessage(self.label_error_option, "#00ff00", "Config Exporter"))
        self.tm.thread("confImport", target=lambda: sendMessage(self.label_error_option, "#00ff00", "Config Importer"))
        self.tm.thread("lang", target=lambda: sendMessage(self.label_error_option, "#00ca00", self.langs.t('UI.OPTION_MENU.message_change_lang'), 3))

    def disable(self):
        pass

    def export_conf(self):
        try:
            self.config.exportConfig()
            self.tm.start("confExport")
        except:
            print('export')

    def import_conf(self):
        try:
            self.config.importConfig()
            self.tm.start("confImport")
        except:
            print('import')

    def fixLang(self, event):
        lc = self.langs.getLocaleShort(self.combox_option_lang.get())
        self.config.CONFIG["lang"] = lc
        self.config.saveConfig()
        self.langs.setLang(lc)
        self.log.debug(f"lang : {self.langs.defaultLang}")
        self.event_generate("<<TK_UP.Update>>")
        self.tm.start("lang")

    