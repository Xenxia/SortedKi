#!/usr/bin/env python3

import os, pathlib, sys, ntpath, shutil, webbrowser, platform

from tk_up import *
from tkinter import *
from ImportPyinstaller import Import_pyInst

from tk_up.widgets.tk import Tk_up
from tk_up.widgets.frame import Frame_up
from tk_up.widgets.label import Label_up
from tk_up.widgets.button import Button_up

from tk_up.managerThemes import ManagerThemes
from tk_up.managerWidgets import ManagerWidgets_up

from tk_up.object.image import Wimage

from PyThreadUp import ThreadUP, ThreadManager
from Pylogger import Logger, DEBUG, INFO, Level_s, Context_s, Stack_s
from Pylang import Lang

#Page
from page.option import option
from page.main import main

PLATFORME_SYS = platform.system()
VERSION = "3.0.0b"
APP_NAME = "SortedKi"
ARGS = sys.argv

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='page')

from update import Update
from conf import Config_
from sort import Sorting, NAME_FOLDER_UNSORTED

executionPath = importPyInst.get_execute_path()

try:
    argDebug = ARGS[1]
except:
    argDebug = ""

try:
    argFile = ARGS[2]
except:
    argFile = ""

log = Logger(
    format="{time} | {levelname} : {stack}{msg}",
    levellog=DEBUG if argDebug == "debug" else INFO,
    file_path="./debug.log" if argFile == "file" else None
)

log.customize(level=Level_s("[", "]"), context=Context_s("{ ", " } "), stack=Stack_s("( ", " ) ", 2, "/", False))

if importPyInst.is_compiled:
    pathAppExe = os.path.realpath(sys.executable)
else:
    log.activColor(True)
    pathAppExe = os.path.realpath(__file__)

pathDirExe = ntpath.dirname(pathAppExe)

log.debug(f"{PLATFORME_SYS}", "OS")
log.debug(f"{executionPath}", "EXE_PATH")

nameAppExe = ntpath.basename(pathAppExe)

conf = Config_(log, pathDirExe)
conf.loadConfig()

langageTask = ThreadUP(target=lambda: Lang(f"{executionPath}/lang"), returnValue=True).start()

# langageTask = ThreadUP(target=lambda: Lang_app(log, conf.CONFIG, path=executionPath), returnValue=True).start()
updateTask = ThreadUP(target=Update, args=(log,), returnValue=True).start()

# langage1: Lang = langageTask2.join()
langage: Lang = langageTask.join()
log.info("Load Language")
update: Update = updateTask.join()
log.info(f"Version latest {update.get_version()}")

langage.setLang(conf.CONFIG["lang"])

tm = ThreadManager()

def openWeb():
    webbrowser.open(f'https://github.com/Xenxia/{APP_NAME}/releases/latest')

def sortedToRoot():
    for name_profile in conf.CONFIG['config_sort']:
        for rule in ["*.*", "*"]:
            path = conf.CONFIG['config_sort'][name_profile]['fullPath']

            for file_path in pathlib.Path(path).rglob(rule):
                file_name = os.path.basename(file_path)
                if os.path.isfile(str(file_path)):
                    shutil.move(str(file_path), './'+str(file_name))
    log.info("Sorted to root", "SORTED-TO-ROOT")

def unsortedToRoot():
    for rule in ["*.*", "*"]:
        for file_path in pathlib.Path(f"./{NAME_FOLDER_UNSORTED}").rglob(rule):
            file_name = os.path.basename(file_path)
            if os.path.isfile(str(file_path)):
                shutil.move(str(file_path), './'+str(file_name))
    log.info("Unsorted to root", "UNSORTED-TO-ROOT")

def notDev():
    main_menu_w.console1.printLastLine("This feature is not developed", color=["Purple"])


# function Sorting
def sortMain():

    log.info("Start", "SORT-MAIN")
    main_menu_w.button_tree.disable()

    try:
        s = Sorting(log, langage, conf, pathDirExe, nameAppExe, main_menu_w)
        s.start()
    except Exception as e:
        log.error(e)

    main_menu_w.button_tree.enable()

##### THREAD #####

tm.thread("sort", target=sortMain)

##### TK     #####------------------------------------------------------------------------------->

# main window
window = Tk_up()

window.configWindows(title=f"{APP_NAME} | {pathDirExe}", geometry="700x700+center", iconbitmap=f"{executionPath}/img/icon.ico")

# window.iconbitmap()
# window.config(background='#202020')
# window.geometry("600x600")
window.resizable(0, 0)
# window.wm_attributes("-transparentcolor", "#123456")
# window.option_add("*font", 'Consolas 10 bold')
# window.columnconfigure(0, weight=1)
# window.rowconfigure(2, weight=1)

theme = ManagerThemes(window, themes_folder=f"{executionPath}/themes").setTheme("dark")

# log.debug(theme.get_theme_use())
# log.debug(theme.get_info_element('listbox'))
# exit()
context = {
    "lib": [langage, conf, log],
    "exe_path": executionPath,
    "sort_func": sortMain,
    "screenMain": window,
    "tm": tm,
    "app_name": APP_NAME
}

main_frame = ManagerWidgets_up(master=window, asset_folder=f"{executionPath}/page", context=context, width=700, height=670)
main_frame.showWidget("main")
main_frame.gridPosSize(0, 0, sticky=(E, W, S, N)).show()

main_menu_w: main = main_frame.getClassWidget("main")
# main_menu_w.button_clear.configure(command=sortMa)
menu_option_w: option = main_frame.getClassWidget("option")
menu_option_w.button_sortedToRoot.configure(command=sortedToRoot)
menu_option_w.button_unsortedToRoot.configure(command=unsortedToRoot)

footer = Frame_up(master=window, width=700, height=30)
footer.propagate(False)
footer.gridPosSize(1, 0, sticky=(S)).show()
# footer.columnconfigure(3, weight=1)
# footer.rowconfigure(0, weight=1)
# style = ttk.Style(window)

#LANG
label_lang = Label_up(footer, text=f"{langage.t('UI.MAIN_MENU.lang')} : {langage.selectedLang}")
label_lang.placePosSize(x=350, y=16, width=120, height=32, anchor="center").show()

#VERSION
frame_version = Frame_up(master=footer, borderwidth=0)
# frame_version.propagate(False)
# frame_version.grid_propagate(False)
frame_version.placePosSize(x=640, y=18.5, width=126, height=32, anchor="center").show()

last_version = update.get_version()

label_version_text = Label_up(frame_version, text="version :")
label_version_text.gridPosSize(row=0, column=0, sticky=W).show()

label_version = Button_up(frame_version, state=DISABLED, text=VERSION, width=7, style="version.TButton")
label_version.gridPosSize(row=0, column=1, pady=(0, 0)).show()

if last_version != "none" and last_version != VERSION:
    label_version.config(state=NORMAL, command=openWeb)

# #main
# button_tree = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_sort'], command=lambda: Thread(target=sort).start())
# button_tree.placePosSize(x=255, y=0, width=90, height=24)

# button_clear = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_clear'], command=lambda: console1.clearTerminal())
# button_clear.placePosSize(x=255, y=24, width=90, height=24)

button_option = Button_up(master=footer, image=Wimage(executionPath + '/img/option.png', (26, 26)), command=lambda: main_frame.showWidget("option"), style="nobg.TButton")
button_option.placePosSize(x=16, y=16, width=32, height=32, anchor="center").show()


log.debug(str(main_frame.addInContextInOneWidget("main", addCtx=("btn_option", button_option))), "addInCtx")
# log.debug(str(window.event_info()), "event")

# mainUi()
window.update()
window.mainloop()

tm.kill_all()