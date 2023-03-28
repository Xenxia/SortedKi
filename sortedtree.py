#!/usr/bin/env python3

import os, pathlib, sys, ntpath, shutil, webbrowser, platform
from tkinter import *
from ImportPyinstaller import Import_pyInst
from PyThreadUp import ThreadUP, ThreadManager
from PIL import Image, ImageTk
from tk_up.widgets import Button_up, Frame_up, Label_up, Tk_up
from tk_up.managerThemes import ManagerThemes
from tk_up.managerWidgets import ManagerWidgets_up
from page.menu_option import menu_option
from page.menu_sort import menu_sort

PLATFORME_SYS = platform.system()
VERSION = "2.0.0"
APP_NAME = "SortedTree"

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='page')

from update import Update
from conf import ConfigTree
from langages import Lang_app
from logger import DEBUG, Logger

notSortList = ["config.yml", "desktop.ini"]

exe_path = importPyInst.get_execute_path()

log = Logger(format="{time} | {levelname} : {msg}", levellog=DEBUG)
log.customize(level=("[", "]"))

if importPyInst.is_compiled:
    path_file = os.path.realpath(sys.executable)
else:
    log.activColor(True)
    path_file = os.path.realpath(__file__)

path_dir_exe = ntpath.dirname(path_file)

log.debug(f"OS : {PLATFORME_SYS}")

exe_file = ntpath.basename(path_file)

conf = ConfigTree(log, path_dir_exe)
conf.loadConfig()

langage_task = ThreadUP(target=lambda: Lang_app(log, conf.CONFIG, path=exe_path), returnValue=True).start()
update_task = ThreadUP(target=Update, args=(log,), returnValue=True).start()

langage: Lang_app = langage_task.join()
update: Update = update_task.join()

tm = ThreadManager()

def openWeb():
    webbrowser.open(f'https://github.com/Xenxia/{APP_NAME}/releases/latest')

def moveToRoot():
    for name_profile in conf.CONFIG['config_sort']:
        for rule in ["*.*", "*"]:
            path = conf.CONFIG['config_sort'][name_profile]['fullPath']

            for file_path in pathlib.Path(path).rglob(rule):
                file_name = os.path.basename(file_path)
                if os.path.isfile(file_path):
                    shutil.move(str(file_path), './'+str(file_name))
    log.info("Move to root")

# def deletConfig():
#     try:
#         os.remove(f"./{conf.CONFIG_FILE_NAME}")
#         Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Config file delete")).start()
#     except:
#         Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Error")).start()

def notSort():
    list_temp = []
    for f in conf.CONFIG["doNotSort"]:
        for file in pathlib.Path('./').glob(f):
            list_temp.append(str(file))
    return list_temp

def duplicate(file: str, path: str) -> str:

    fileName, fileExt = os.path.splitext(file)

    pathFile = f"{path}/{file}"

    numberDuplicate = 1
    end = False
    index = 0
    forcePass = False

    while os.path.exists(pathFile):

        if fileName[-1] != "]" or forcePass:
            newName = f"{fileName}_[{numberDuplicate}]"
            numberDuplicate += 1
        else:
            if not end:
                if "_[" in fileName and "]" in fileName:
                    for i in range(12+4):
                        i_N = (i*-1)
                        if "_[" == fileName[i_N:(i_N+2)]:
                            index = i
                            end = True
                            break
                try:
                    number = int(fileName[-(index-2):-1])
                except ValueError:
                    forcePass = True
                    newName = fileName
                fileNameNoNumber = fileName[0:-index]

            if not forcePass:
                newName = f"{fileNameNoNumber}_[{number+numberDuplicate}]"
                numberDuplicate += 1

        pathFile = f"{path}/{newName}{fileExt}"

    # os.rename(file, pathFile)
    

    # while True:
        # if numWhile != 0:
        #     new_name = new_name.replace(new_name[-2:], "_"+str(numWhile))
        # else:
        #     if fileName[-2]!="_":
        #         new_name = fileName+'_'+str(numWhile)
        #     else:
        #         new_name = fileName.replace(fileName[-2:], "_"+str(numWhile+1))

        # new_path = path+'/'+new_name+fileExt
        # if not os.path.exists(new_path):
        #     os.rename(fileName+fileExt, new_path)
        #     break
        # numWhile += 1

    return newName+fileExt

def notDev():
    main_menu_w.console1.printLastLine("This feature is not developed", color=["Purple"])


# function Sorting
def sortMain():

    log.debug("SORT")

    main_menu_w.button_tree.disable()

    notSort_userConfig = notSort()

    check: list = []

    for name_profile in conf.CONFIG['config_sort']:

        disable = conf.CONFIG['config_sort'][name_profile]['disable']

        for rule in conf.CONFIG['config_sort'][name_profile]['rule']:
            config_path: str = conf.CONFIG['config_sort'][name_profile]['fullPath']
            pathStatic: bool = conf.CONFIG['config_sort'][name_profile]['pathStatic']

            parent_path = path_dir_exe

            if not os.path.exists(f"{path_dir_exe}/{config_path}"):
                os.makedirs(f"{path_dir_exe}/{config_path}", exist_ok=True)

            if rule == "":
                break

            sort(rule, notSort_userConfig, check, config_path, parent_path, pathStatic, disable)

    if conf.CONFIG['unsorted'] == True :
        if not os.path.exists(f"{path_dir_exe}/#Unsorted"):
            os.mkdir(f"{path_dir_exe}/#Unsorted")

        sort_unsorted(notSort_userConfig, check)

    main_menu_w.button_tree.enable()

def sort(rule: str, notSort_userConfig: list, check: list, config_path: str, search_path: str, static_path: bool, disable: bool):

    # log.debug(rule)

    for file in pathlib.Path(search_path).glob(rule):

        file_name = ntpath.basename(file)

        parent_path = f"{search_path}/{config_path}"

        file_futur_path = f"{parent_path}/{file_name}"

        if static_path:
            parent_path = f"{config_path}"
            file_futur_path = f"{config_path}/{file_name}"

        log.debug(file)
        log.debug(file_name)
        log.debug(file_futur_path)

        duplica = False
        sort = False
        permission = False
        new = "new"
        err = [False, "none"]

        if str(file_name) not in notSort_userConfig and str(file_name) not in notSortList and str(file_name) != exe_file:

            check.append(str(file_name))

            if not disable:
                return

            if not os.path.exists(file_futur_path):

                try:
                    if os.path.isfile(file_name):

                        shutil.move(str(file_name), file_futur_path)
                        sort = True
                    else:
                        break

                # For permission related errors
                except PermissionError:
                    permission = True

                # For other errors
                except OSError as error:
                    err = [True, error]

            else:
                try:
                    if os.path.isfile(file_name):
                        new = duplicate(str(file_name), f"{parent_path}")
                        shutil.move(src = file_name, dst = f"{parent_path}/{new}")
                        sort, duplica = True, True
                    else:
                        break

                except PermissionError:
                    permission = True
                    
                # For other errors
                except OSError as error:
                    err = [True, error]

        if sort and not duplica:
            main_menu_w.console1.printLastLine("✔: ", langage.lang['OK']['sorted'].format(file=str(file_name), path=config_path), color=["Green", None])

        if sort and duplica:
            main_menu_w.console1.printLastLine("✔: ", langage.lang['OK']['sorted_double'].format(file=str(file_name), new_name=new, path=config_path), color=["Blue", None])

        if permission:
            main_menu_w.console1.printLastLine("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file_name)), color=["Orange", None])

        if err[0]:
            main_menu_w.console1.printLastLine("❌: ", str(err[1]), color=["Red", None])
            log.error("❌: " + str(err[1]))

def sort_unsorted(notSort_userConfig, check):
    for file_path in pathlib.Path(path_dir_exe).glob('*.*'):

        file_name = ntpath.basename(file_path)

        log.debug(check)

        if str(file_name) not in notSort_userConfig and str(file_name) not in notSortList and str(file_name) not in check and str(file_name) != exe_file:

            try:
                os.rename(str(file_name), f"{path_dir_exe}/#Unsorted/{str(file_name)}")
                main_menu_w.console1.printLastLine("✔: ", langage.lang['OK']['unsorted'].format(file=str(file_name)), color=["Purple", None])

            # For permission related errors
            except PermissionError:
                main_menu_w.console1.printLastLine("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file_name)), color=["Orange", None])

            # For File Exists errors
            except FileExistsError:
                new = duplicate(str(file_name), f"{path_dir_exe}/#Unsorted")
                shutil.move(src = str(file_name), dst = f"{path_dir_exe}/#Unsorted/{new}")
                main_menu_w.console1.printLastLine("✔: ", langage.lang['OK']['sorted_double_unsorted'].format(file=str(file_name), new_name=new), color=["Purple2", None])

            # For other errors
            except OSError as error:
                main_menu_w.console1.printLastLine("❌: ", str(error), color=["Red", None])
                log.error("❌: " + str(error))


##### THREAD #####

tm.thread("sort", target=sortMain)


##### # ? TK ------------------------------------------------------------------------------->

# main window
window = Tk_up()

window.configWindows(title=f"{APP_NAME} | {path_dir_exe}", geometry="700x700+center", iconbitmap=f"{exe_path}/img/tree.ico")

# window.iconbitmap()
# window.config(background='#202020')
# window.geometry("600x600")
window.resizable(0, 0)
# window.wm_attributes("-transparentcolor", "#123456")
# window.option_add("*font", 'Consolas 10 bold')
# window.columnconfigure(0, weight=1)
# window.rowconfigure(2, weight=1)

theme = ManagerThemes(window, themes_folder=f"{exe_path}/themes").setTheme("sortedtree", "dark")

# log.debug(theme.get_theme_use())
# log.debug(theme.get_info_element('B.TFrame'))
# exit()
param_d = {
    "exe_path": exe_path,
    "sort_func": sortMain,
    "screenMain": window,
    "tm": tm,
}

main_frame = ManagerWidgets_up(master=window, asset_folder=f"{exe_path}/page", parameters_list=[langage, conf, log], parameters_dict=param_d, width=700, height=670)
main_frame.showWidget("menu_sort")
main_frame.gridPosSize(0, 0, sticky=(E, W, S, N)).show()

main_menu_w: menu_sort = main_frame.getClassWidget("menu_sort")
# main_menu_w.button_clear.configure(command=sortMa)
menu_option_w: menu_option = main_frame.getClassWidget("menu_option")
menu_option_w.button_moovToRoot.configure(command=moveToRoot)

footer = Frame_up(master=window, width=700, height=30)
footer.propagate(False)
footer.gridPosSize(1, 0, sticky=(S)).show()
# footer.columnconfigure(3, weight=1)
# footer.rowconfigure(0, weight=1)
# style = ttk.Style(window)

image = Image.open(exe_path + '/img/option.png')
# image = image.resize((32, 32), Image.ANTIALIAS)
option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_up(footer, text=f"{langage.lang['UI']['MAIN_MENU']['lang']} : {langage.get_locale_ac()}")
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

button_option = Button_up(master=footer, image=option_image, command=lambda: main_frame.showWidget("menu_option"), style="nobg.TButton")
button_option.placePosSize(x=16, y=16, width=32, height=32, anchor="center").show()


main_frame.addParametersInOneWidget("menu_sort", parameter_list=button_option)


# mainUi()
window.update()
window.mainloop()

tm.kill_all()