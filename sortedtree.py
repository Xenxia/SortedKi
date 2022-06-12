#!/usr/bin/env python3

import os, pathlib, sys, ntpath, shutil, webbrowser, platform
from time import sleep
from tkinter import *
from tkinter import ttk
from ImportPyinstaller import Import_pyInst
from PyThreadUp import ThreadUP
from threading import Thread
from PIL import Image, ImageTk
from tk_up.widgets import SCROLL_ALL, Button_up, Entry_up, Frame_up, Label_up, OptionMenu_up, Terminal_ScrolledText_up, Tk_up, Toggle_Button_up, Toplevel_up, Treeview_up, Widget_up
from tk_up.managerThemes import ManagerThemes
from tk_up.managerWidgets import ManagerWidgets_up
from page.menu_sort import menu_sort


importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='page')

PLATFORME_SYS = platform.system()
VERSION = "1.1.1"
APP_NAME = "SortedTree"

notSortList = ["config.yml", "desktop.ini"]

exe_path = importPyInst.get_execute_path()

from update import Update
from conf import ConfigTree
from langages import LANG_AC, Lang_app
from logger import DEBUG, INFO, Logger

log = Logger(format="{time} | {levelname} : {msg}", levellog=DEBUG)
log.customize(level=("[", "]"))

if importPyInst.is_compiled:
    path_file = os.path.realpath(sys.executable)
else:
    log.activColor(True)
    path_file = os.path.realpath(__file__)

log.debug(f"OS : {PLATFORME_SYS}")

exe_file = ntpath.basename(path_file)

conf = ConfigTree(log)
conf.loadConfig()

langage_task = ThreadUP(target=lambda: Lang_app(log, conf.CONFIG, path=exe_path), returnValue=True).startTask()
update_task = ThreadUP(target=Update, args=(log,), returnValue=True).startTask()

langage: Lang_app = langage_task.join()
update: Update = update_task.join()

def openWeb():
    webbrowser.open(f'https://github.com/Xenxia/{APP_NAME}/releases/latest')

def sendMessage(label: Label_up, color: str, message: str, time: int=7):
    label.config(fg=color, text=message)
    label.show()
    sleep(time)
    label.config(fg="#202020", text="")
    label.hide()

def export_conf():
    try:
        conf.exportConfig()
        Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Config Exporter")).start()
    except:
        print('export')

def import_conf():
    try:
        conf.importConfig()
        Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Config Importer")).start()
    except:
        print('import')

def moveToRoot():
    for name_profile in conf.CONFIG['config_sort']:
        for rule in ["*.*", "*"]:
            path = conf.CONFIG['config_sort'][name_profile]['fullPath']

            for file_path in pathlib.Path(path).rglob(rule):
                file_name = os.path.basename(file_path)
                if os.path.isfile(file_path):
                    shutil.move(str(file_path), './'+str(file_name))
    log.info("Move to root")

def deletConfig():
    try:
        os.remove(f"./{conf.CONFIG_FILE_NAME}")
        Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Config file delete")).start()
    except:
        Thread(target=lambda: sendMessage(label_error_option, "#00ff00", "Error")).start()

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
    console1.printTerminal("This feature is not developed", color=["Purple"])

def sort():

    main_menu_w.button_tree.disable()

    notSort_userConfig = notSort()

    check: list = []

    for name_profile in conf.CONFIG['config_sort']:
        for rule in conf.CONFIG['config_sort'][name_profile]['ext']:
            path = conf.CONFIG['config_sort'][name_profile]['fullPath']

            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

            if rule == "":
                break

            for file in pathlib.Path('./').glob(rule):

                duplica = False
                sort = False
                permission = False
                new = "new"
                err = [False, "none"]

                if str(file) not in notSort_userConfig and str(file) not in notSortList and str(file) != exe_file:

                    check.append(str(file))

                    if not os.path.exists(f"{path}/{file}"):

                        try:
                            if os.path.isfile(file):

                                shutil.move(str(file), path+'/'+str(file))
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
                            if os.path.isfile(file):
                                new = duplicate(str(file), path)
                                shutil.move(src = file, dst = path+'/'+str(new))
                                sort, duplica = True, True
                            else:
                                break

                        except PermissionError:
                            permission = True
                            
                        # For other errors
                        except OSError as error:
                            err = [True, error]

                if sort and not duplica:
                    main_menu_w.console1.printTerminal("✔: ", langage.lang['OK']['sorted'].format(file=str(file), path=path), color=["Green", None])

                if sort and duplica:
                    main_menu_w.console1.printTerminal("✔: ", langage.lang['OK']['sorted_double'].format(file=str(file), new_name=new, path=path), color=["Blue", None])

                if permission:
                    main_menu_w.console1.printTerminal("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file)), color=["Orange", None])

                if err[0]:
                    main_menu_w.console1.printTerminal("❌: ", str(err[1]), color=["Red", None])
                    log.error("❌: " + str(error))

    if conf.CONFIG['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):

            if str(file) not in notSort_userConfig and str(file) not in notSortList and str(file) not in check and str(file) != exe_file:

                try:
                    os.rename(str(file), './#Unsorted/'+str(file))
                    main_menu_w.console1.printTerminal("✔: ", langage.lang['OK']['unsorted'].format(file=str(file)), color=["Purple", None])

                # For permission related errors
                except PermissionError:
                    main_menu_w.console1.printTerminal("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file)), color=["Orange", None])

                # For File Exists errors
                except FileExistsError:
                    new = duplicate(str(file), "./#Unsorted")
                    main_menu_w.console1.printTerminal("✔: ", langage.lang['OK']['sorted_double_unsorted'].format(file=str(file), new_name=new), color=["Purple2", None])

                # For other errors
                except OSError as error:
                    main_menu_w.console1.printTerminal("❌: ", str(error), color=["Red", None])
                    log.error("❌: " + str(error))
    del check
    main_menu_w.button_tree.enable()

# # ? TK ------------------------------------------------------------------------------->

# def mainUi():
#     console1.show()
#     button_tree.show()
#     button_clear.show()
#     button_option.show()
#     button_option.enable()

#     button_edit.hide()
#     button_export.hide()
#     button_import.hide()
#     button_return.hide()
#     button_moveToRoot.hide()
#     button_deleteConfig.hide()

#     ihm.hide()
#     button_saveAndReturn.hide()

# #Option
# def optionUi():
#     console1.hide()
#     button_tree.hide()
#     button_clear.hide()
#     button_option.show()
#     button_option.disable()

#     button_edit.show()
#     button_export.show()
#     button_import.show()
#     button_return.show()
#     button_moveToRoot.show()
#     button_deleteConfig.show()

#     ihm.hide()
#     button_saveAndReturn.hide()

# def fixLang(event):
#     conf.CONFIG["lang"] = langage.get_local_ac_from_name_lang(combox_option_lang.get())
#     conf.saveConfig()
#     Thread(target=lambda: sendMessage(label_error_option, "#00ca00", langage.lang['UI']['OPTION_MENU']['message_change_lang'], 3)).start()

# #Edit
# def editUi():
#     console1.hide()
#     button_tree.hide()
#     button_clear.hide()
#     button_option.hide()

#     button_edit.hide()
#     button_export.hide()
#     button_import.hide()
#     button_return.hide()
#     button_moveToRoot.hide()
#     button_deleteConfig.hide()

#     for i in ihm.treeView.tree.get_children():
#         ihm.treeView.tree.delete(i)

#     for key in conf.CONFIG['config_sort']:
#         folder: str = conf.CONFIG['config_sort'][key]['folder']
#         extention: list = conf.CONFIG['config_sort'][key]['ext']
#         parent: str | None = conf.CONFIG['config_sort'][key]['parent']

#         parent = parent if parent is not None else ''

#         # ihm.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(extention)))
#         ihm.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(extention)])

#     ihm.toggle_b.set_default_status(conf.CONFIG["unsorted"])
#     doNotSort = "|".join(conf.CONFIG["doNotSort"])
#     if not doNotSort == "":
#         ihm.doNotSort_box.delete(0, END)
#         ihm.doNotSort_box.insert(0, doNotSort)

#     ihm.show()
#     button_saveAndReturn.show()

# def unselect():
#     try:
#         ihm.edit.disable()
#         ihm.remove.disable()
#         ihm.unselect.disable()
#         ihm.move_up.disable()
#         ihm.move_down.disable()
#         ihm.treeView.tree.selection_remove(ihm.treeView.tree.selection()[0])
#     except:
#         print("not select")

# def delete():
#     ihm.treeView.removeSelectedElement()
#     unselect()

# #Toplevel menu
# def editMenu():

#     addEditWindow.title(langage.lang['UI']['EDIT_MENU']['title_edit'])

#     addOrEdit.config(text=langage.lang['UI']['EDIT_MENU']['button_apply'])

#     profile_box.delete(0, END)
#     folder_box.delete(0, END)
#     rule_box.delete(0, END)

#     addOrEdit.config(command=edit)

#     try:
#         selected = ihm.treeView.getItemSelectedElemnt()
#         # values = self.treeView.tree.item(selected, 'values')

#         # output to entry boxes
#         profile_box.insert(0, selected[0])
#         folder_box.insert(0, selected[1])
#         rule_box.insert(0, selected[2])
        

#         addEditWindow.show()

#     except:
#         print("not select")

# def edit():
#     try:
#         selected = ihm.treeView.tree.selection()[0]
#         ihm.treeView.tree.item(selected, text=profile_box.get(), values=(folder_box.get(), rule_box.get()))
#         addEditWindow.hide()
#     except:
#         Thread(target=lambda: sendMessage(label_error_edit, "#ff3030", f"no items selected")).start()

# def addMenu():
#     addEditWindow.title(langage.lang['UI']['EDIT_MENU']['title_add'])

#     addOrEdit.config(text=langage.lang['UI']['EDIT_MENU']['button_add'])

#     profile_box.delete(0, END)
#     folder_box.delete(0, END)
#     rule_box.delete(0, END)

#     addOrEdit.config(command=add)

#     addEditWindow.show()

# def add():
#     profile_name = profile_box.get()
#     folder = folder_box.get()
#     rule = rule_box.get()

#     sellect = ""

#     try:
#         sellect = ihm.treeView.tree.selection()[0]
#     except:
#         log.debug("No select")

#     if profile_name!="" and folder!="":
#         try:
#             ihm.treeView.tree.insert(parent=sellect, index=END, iid=profile_name, text=profile_name, values=(folder, rule), tags=('evenrow',))
#             unselect()
#             addEditWindow.hide()
#         except:
#             Thread(target=lambda: sendMessage(label_error_addEditWindow, "#ff3030", f"The profile {profile_name} already exists")).start()

#     else:
#         Thread(target=lambda: sendMessage(label_error_addEditWindow, "#ff3030", f"Profile name and Folder is required")).start()
#         log.debug("Profile name and Folder is required")


# main window
window = Tk_up()

window.configWindows(title=f"{APP_NAME} | {ntpath.dirname(path_file)}", geometry="700x700+center", iconbitmap=f"{exe_path}/img/tree.ico")

# window.iconbitmap()
# window.config(background='#202020')
# window.geometry("600x600")
window.resizable(0, 0)
# window.option_add("*font", 'Consolas 10 bold')
# window.columnconfigure(0, weight=1)
# window.rowconfigure(0, weight=1)

# theme = ManagerThemes(window).setTheme("azure", themes="dark")

main_frame = ManagerWidgets_up(master=window, asset_folder=f"{exe_path}/page", parameters=[langage, conf, log], width=700, height=670)
main_frame.showWidget("menu_sort")
main_frame.gridPosSize(0, 0, sticky=(E, W, S, N)).show()

log.debug(main_frame.class_widget)

main_menu_w: menu_sort = main_frame.getClassWidget("menu_sort")
main_menu_w.button_tree.configure(command=sort)


footer = Frame_up(master=window, width=700, height=30)
# footer.propagate(False)
footer.gridPosSize(1, 0, sticky=(E, W, S, N)).show()
# footer.columnconfigure(3, weight=1)
# footer.rowconfigure(0, weight=1)
# style = ttk.Style(window)

# addEditWindow = Toplevel_up(window)
# addEditWindow.geometry("600x95")
# addEditWindow.iconbitmap(f"{exe_path}/img/tree.ico")
# addEditWindow.config(background='#202020')
# addEditWindow.resizable(0, 0)
# addEditWindow.hide()

# #Labels
# nl = Label_up(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_name_profil'], bg="#202020", fg="#00ca00")
# nl.gridPosSize(row=0, column=0, sticky=W).show()

# il = Label_up(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_folder'], bg="#202020", fg="#00ca00")
# il.gridPosSize(row=1, column=0, sticky=W).show()

# tl = Label_up(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_extention'], bg="#202020", fg="#00ca00")
# tl.gridPosSize(row=2, column=0, sticky=W).show()

# #Entry boxes
# profile_box = Entry_up(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
# profile_box.gridPosSize(row=0, column=1, sticky=W).show()

# folder_box = Entry_up(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
# folder_box.gridPosSize(row=1, column=1, sticky=W).show()

# rule_box = Entry_up(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
# rule_box.gridPosSize(row=2, column=1, sticky=W).show()

# buttonF = Frame_up(addEditWindow)

# addOrEdit = Button_up(buttonF, bg="#555555", fg="#00ca00", activebackground="#555555")
# addOrEdit.gridPosSize(row=0, column=0).show()

# cancel = Button_up(buttonF, text=langage.lang['UI']['EDIT_MENU']['button_cancel'], bg="#555555", fg="#00ca00", activebackground="#555555", command=addEditWindow.hide)
# cancel.gridPosSize(row=0, column=1).show()

# buttonF.gridPosSize(row=3, column=1, sticky=W).show()

# #STYLE



# # custom indicator images
# im_open = Image.open(exe_path + '/img/moins.png')
# im_open = im_open.resize((15, 15), Image.ANTIALIAS)
# im_close = Image.open(exe_path + '/img/plus.png')
# im_close = im_close.resize((15, 15), Image.ANTIALIAS)
# im_empty = Image.new('RGBA', (15, 15), '#00000000')

# img_open = ImageTk.PhotoImage(im_open, name='img_open', master=window)
# img_close = ImageTk.PhotoImage(im_close, name='img_close', master=window)
# img_empty = ImageTk.PhotoImage(im_empty, name='img_empty', master=window)

# # custom indicator
# style.element_create('Treeitem.myindicator',
#             'image', img_close, ('user1', '!user2', img_open), ('user2', img_empty),
#             sticky='w', width=20)

# # replace Treeitem.indicator by custom one
# style.layout('Treeview.Item',
#         [('Treeitem.padding',
#         {'sticky': 'nswe',
#         'children': [('Treeitem.myindicator', {'side': 'left', 'sticky': ''}),
#             ('Treeitem.image', {'side': 'left', 'sticky': ''}),
#             ('Treeitem.focus',
#             {'side': 'left',
#             'sticky': '',
#             'children': [('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})]
#         )

# image = Image.open(exe_path + '/img/option.png')
# image = image.resize((24, 24), Image.ANTIALIAS)
# option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_up(footer, text=f"{langage.lang['UI']['MAIN_MENU']['lang']} : {langage.get_locale_ac()}")
label_lang.placePosSize(x=350, y=16, width=124, height=32, anchor="center").show()

# #LABEL ERROR
# label_error_option = Label_up(window, text="", bg='#202020', fg='#202020')
# label_error_option.placePosSize(x=0, y=270, width=600, height=32)

# label_error_edit = Label_up(window, text="", bg='#202020', fg='#202020')
# label_error_edit.placePosSize(x=0, y=410, width=600, height=32)

# label_error_addEditWindow = Label_up(addEditWindow, text="", bg='#202020', fg='#ffffff')
# label_error_addEditWindow.placePosSize(x=200, y=63, width=300, height=32)

#VERSION
frame_version = Frame_up(master=footer, borderwidth=0)
# frame_version.propagate(False)
# frame_version.grid_propagate(False)
frame_version.placePosSize(x=630, y=18.5, width=124, height=32, anchor="center").show()

last_version = update.get_version()

label_version_text = Label_up(frame_version, text="version :")
label_version_text.gridPosSize(row=0, column=0, sticky=W).show()

label_version = Button_up(frame_version, state=DISABLED, text=VERSION, width=7)
label_version.gridPosSize(row=0, column=1, pady=(1, 0)).show()

if last_version != "none" and last_version != VERSION:
    label_version.config(state=NORMAL, command=openWeb)

# #main
# button_tree = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_sort'], command=lambda: Thread(target=sort).start())
# button_tree.placePosSize(x=255, y=0, width=90, height=24)

# button_clear = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_clear'], command=lambda: console1.clearTerminal())
# button_clear.placePosSize(x=255, y=24, width=90, height=24)

# button_option = Button_up(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=optionUi)
# button_option.placePosSize(x=2, y=574, width=24, height=24)

# #option
# button_edit = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_edit'], command=editUi)
# button_edit.placePosSize(x=210, y=24, width=180, height=24)

# button_export = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_export'], command=export_conf)
# button_export.placePosSize(x=210, y=48, width=180, height=24)

# button_import = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_import'], command=import_conf)
# button_import.placePosSize(x=210, y=72, width=180, height=24)

# button_moveToRoot = Button_up(window, bg="#555555", fg="#ff3030", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_move_root'], command=moveToRoot)
# button_moveToRoot.placePosSize(x=210, y=124, width=180, height=24)

# button_deleteConfig = Button_up(window, bg="#555555", fg="#ff3030", wraplength=180, activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_delete_conf'], command=deletConfig)
# button_deleteConfig.placePosSize(x=210, y=148, width=180)

# combox_option_lang = OptionMenu_up(window, default=0, list=[key for key in LANG_AC.keys()], justify='center')
# combox_option_lang.current(langage.index)
# combox_option_lang.bind("<<ComboboxSelected>>", fixLang)
# combox_option_lang.placePosSize(x=235, y=210,width=130, height=24).show()

# button_return = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_return'], command=mainUi)
# button_return.placePosSize(x=235, y=250, width=130, height=24)

# #CONSOLE
# colorConsole = {
#     "Green": ["#000000", "#00ff00"],
#     "Blue": ["#000000", "#26abff"],
#     "Orange": ["#000000", "#ff7f00"],
#     "Red": ["#000000", "#ff0000"],
#     "Purple": ["#000000", "#ff0aff"],
#     "Purple2": ["#000000", "#743DFF"]
# }
# console1 = Terminal_ScrolledText_up(window, bg="#000000", fg="#FFFFFF")
# console1.configTag(colorConsole)
# console1.placePosSize(x=0, y=48, width=600, height=524)

# #tab config

# class IHM(Frame, Widget_up):

#     def __init__(self, master=None, cnf={}, **kw) -> None:
#         Frame.__init__(self, master=master, cnf=cnf, **kw)
#         Widget_up.__init__(self)

#         self.frameButton = Frame_up(self, bg="#202020")
#         self.frameButton.gridPosSize(row=1, column=0, sticky=W).show()

#         self.frameBox = Frame_up(self, bg="#202020", width=600)
#         self.frameBox.gridPosSize(row=2, column=0, sticky=W).show()
#         self.frameBox.propagate(False)
        
#         self.treeView = Treeview_up(self, scroll=SCROLL_ALL, iid=True, child=True, show="tree headings", width=600, height=300)
#         self.treeView.bind("<ButtonRelease-1>", self.selected)
#         self.treeView.gridPosSize(row=0, column=0, sticky=W).show()

#         self.unselect = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_unselect'], command=unselect, bg="#555555", fg="#00ca00", activebackground="#555555")
#         self.unselect.gridPosSize(column=5, row=0, padx=5).show().disable()

#         self.move_up = Button_up(self.frameButton, text="⬆", command=self.treeView.moveUpSelectedElement, bg="#555555", fg="#00ca00", activebackground="#555555")
#         self.move_up.gridPosSize(column=4, row=0).show().disable()

#         self.move_down = Button_up(self.frameButton, text="⬇", command=self.treeView.moveDownSelectedElement, bg="#555555", fg="#00ca00", activebackground="#555555")
#         self.move_down.gridPosSize(column=3, row=0).show().disable()

#         self.remove = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_delete'], command=delete, bg="#555555", fg="#00ca00", activebackground="#555555")
#         self.remove.gridPosSize(column=2, row=0, padx=5).show().disable()

#         self.edit = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_edit'], command=editMenu, bg="#555555", fg="#00ca00", activebackground="#555555")
#         self.edit.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

#         add = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_add'], command=addMenu, bg="#555555", fg="#00ca00", activebackground="#555555")
#         add.gridPosSize(column=0, row=0).show()

#         self.doNotSort_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
#         self.doNotSort_box.grid(row=6, column=1, sticky=W, pady=(13, 0))

#         d1 = Label_up(self.frameBox, text=langage.lang['UI']['EDIT_MENU']['label_not_sort'], bg="#202020", fg="#00ca00")
#         d1.gridPosSize(row=6, column=0, pady=(20, 10), padx=(5, 5)).show()

#         self.toggle_b = Toggle_Button_up(self.frameBox, bg="#555555", activebackground="#555555", width=3)
#         self.toggle_b.custom_toggle(("✔", "✖"))
#         self.toggle_b.gridPosSize(column=1, row=7, sticky=W).show()

#         u1 = Label_up(self.frameBox, text=langage.lang['UI']['EDIT_MENU']['label_unsorted'], bg="#202020", fg="#00ca00")
#         u1.gridPosSize(row=7, column=0, padx=(5, 5)).show()

#         # event
#     def selected(self, event):
#         if self.treeView.getSelectedElement():
#             self.edit.enable()
#             self.remove.enable()
#             self.unselect.enable()
#             self.move_up.enable()
#             self.move_down.enable()

# ihm = IHM(window, bg="#202020")
# ihm.placePosSize(0, 0, 600, 450)
# ihm.treeView.setColumns([
#         langage.lang['UI']['EDIT_MENU']['col_name_profil'],
#         langage.lang['UI']['EDIT_MENU']['col_folder'],
#         langage.lang['UI']['EDIT_MENU']['col_extention']
#     ], 
#     [150, 150, 300]
# )
# ihm.propagate(False)

# def getConfig():

#     conf.CONFIG['config_sort'] = {}

#     for iid in ihm.treeView.getAllChildren().items():
#         key = ""
#         fullPath = ""

#         conf.CONFIG['config_sort'][iid[0]] = {}
#         key = iid[0]

#         value = iid[1]['values']
    
#         conf.CONFIG['config_sort'][key]['parent'] = iid[1]['parent']
#         conf.CONFIG['config_sort'][key]['folder'] = value[0]
#         for index, parent in enumerate(ihm.treeView.getAllParentItem(key)[::-1]):

#             folder = ihm.treeView.getItem(parent)["values"][0]
            
#             if index != 0:
#                 fullPath += f"/{folder}"
#             else:
#                 if folder[0] != "/" and folder[1] != ":":
#                     fullPath += f"./{folder}"
#                 else:
#                     fullPath += f"{folder}"
                

#         conf.CONFIG['config_sort'][key]['fullPath'] = fullPath
#         conf.CONFIG['config_sort'][key]['ext'] = value[1].split("|")



#     conf.CONFIG["unsorted"] = ihm.toggle_b.get_status()
#     doNotSort2 = ihm.doNotSort_box.get()
#     if not doNotSort2 == "":
#         conf.CONFIG["doNotSort"] = doNotSort2.split("|")
#     else:
#         conf.CONFIG["doNotSort"] = []

#     conf.saveConfig()
#     optionUi()

# button_saveAndReturn = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['EDIT_MENU']['buton_return_save'], command=getConfig)
# button_saveAndReturn.placePosSize(x=2, y=574, width=180, height=24)

# mainUi()
window.update()
window.mainloop()