from tkinter import E, W, S, N, CENTER
from tk_up.widgets import Frame_up, Button_up, LabelFrame_up, Label_up, OptionMenu_up
from tk_up.managerWidgets import ManagerWidgets_up
from PyThreadUp import ThreadManager
from Pylogger import Logger
from Pylang import Lang

from func.conf import ConfigTree
from func.function import sendMessage

class option(Frame_up):

    parameters_list: list
    manager_class: ManagerWidgets_up

    #parameters

    log: Logger
    config: ConfigTree
    langs: Lang

    def __init__(self, parameters_list: list,  parameters_dict: dict, manager_class: ManagerWidgets_up, master=None, kw={"width":0, "height":0}):
        self.parameters_list = parameters_list.copy()
        self.parameters_dict = parameters_dict
        self.manager_class = manager_class

        self.tm: ThreadManager = self.parameters_dict["tm"]

        self.langs: Lang = parameters_list[0]
        self.config: ConfigTree = parameters_list[1]
        self.log: Logger = parameters_list[2]

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N))
        #command=lambda: Thread(target=sort).start()

        # Settings
        self.frame_config = LabelFrame_up(self, text=self.langs.t('UI.OPTION_MENU.frame_config'))
        self.frame_config.placePosSize(350, 100, 120, 140, anchor="center").show()
        self.frame_config.columnconfigure(0, weight=1)
        self.frame_config.rowconfigure(3, weight=1)

        self.button_export = Button_up(self.frame_config, text=self.langs.t('UI.OPTION_MENU.button_export'), command=self.export_conf)
        self.button_export.gridPosSize(row=0, column=0, sticky=(E, W, S, N), pady=(6,0)).show()

        self.button_import = Button_up(self.frame_config, text=self.langs.t('UI.OPTION_MENU.button_import'), command=self.import_conf)
        self.button_import.gridPosSize(row=1, column=0, sticky=(E, W, S, N), pady=(3,0)).show()

        self.button_edit = Button_up(self.frame_config, text=self.langs.t('UI.OPTION_MENU.button_edit'), command=lambda: self.manager_class.showWidget("edit_settings"))
        self.button_edit.gridPosSize(row=2, column=0, sticky=(E, W, S, N), pady=(3,0)).show()

        self.button_delete = Button_up(self.frame_config, text=self.langs.t('UI.OPTION_MENU.button_delete_conf'), style="fgred.TButton")
        self.button_delete.gridPosSize(row=3, column=0, sticky=(E, W, S, N), pady=(3,10)).show()

        # Warning
        self.frame_function_warning = LabelFrame_up(self, text="Warning")
        self.frame_function_warning.placePosSize(350, 220, 120, 70, anchor="center").show()
        self.frame_function_warning.columnconfigure(0, weight=1)
        self.frame_function_warning.rowconfigure(0, weight=1)

        self.button_moovToRoot = Button_up(self.frame_function_warning, text=self.langs.t('UI.OPTION_MENU.button_move_root'), style="fgred.TButton")
        self.button_moovToRoot.gridPosSize(row=0, column=0, sticky=(E, W, S, N), pady=(5,10)).show()

        # Lang
        self.frame_lang = LabelFrame_up(self, text="lang")
        self.frame_lang.placePosSize(350, 300, 120, 51, anchor="center").show()
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
        self.config.CONFIG["lang"] = self.langs.getLocaleShort(self.combox_option_lang.get())
        self.config.saveConfig()
        self.tm.start("lang")

    