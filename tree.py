#!/usr/bin/env python3

import os, pathlib, sys, ntpath
from tkinter import *
# from tkinter import ttk
from ImportPyinstaller import Import_pyInst
from threading import Thread
from PIL import Image, ImageTk
import webbrowser

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='lang')
importPyInst.add_path(folder_path='image')

version = "0.0.4b"

notSortList = ["config.yml", "desktop.ini"]

exe_path = importPyInst.get_execute_path()

from update import Update
from conf import ConfigTree
from langages import Lang_app
from logger import DEBUG, Logger
from ui import Button_up, Frame_up, Label_up, Terminal_ScrolledText_up, Treeview_up

log = Logger(format="{time} | {levelname} : {msg}", levellog=DEBUG)
log.customize(level=("[", "]"))

if importPyInst.is_compiled:
    exe_file = os.path.realpath(sys.executable)
else:
    log.activColor(True)
    exe_file = os.path.realpath(__file__)

exe_file = ntpath.basename(exe_file)

langage = Lang_app(log, path=exe_path)

update = Update(log)

conf = ConfigTree(log, lang=langage.lang)
conf.loadConfig()

def openWeb():
    webbrowser.open('https://github.com/Xenxia/Tree/releases/latest')

def moveToRoot():
    for file_path in pathlib.Path('./').rglob("*.*"):
        file_name = os.path.basename(file_path)
        os.rename(str(file_path), './'+str(file_name))
    log.info("Move to root")

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

    os.rename(file, pathFile)
    

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

def not_dev():
    console1.printTerminal("This feature is not developed", color=["Purple"])

def sort():

    button_tree.disable()

    notSort_userConfig = notSort()

    check: list = []

    for key in conf.CONFIG['config_sort']:
        for key2 in conf.CONFIG['config_sort'][key]['ext']:
            path = './'+conf.CONFIG['config_sort'][key]['path']

            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

            for file in pathlib.Path('./').glob(key2):

                if str(file) not in notSort_userConfig and str(file) not in notSortList and str(file) != exe_file:

                    check.append(str(file))
                    try:
                        os.rename(str(file), path+'/'+str(file))
                        console1.printTerminal("✔: ", langage.lang['OK']['sorted'].format(file=str(file), path=path), color=["Green", None])

                    # For permission related errors
                    except PermissionError:
                        console1.printTerminal("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file)), color=["Orange", None])

                    # For File Exists errors
                    except FileExistsError:
                        new = duplicate(str(file), path)
                        console1.printTerminal("✔: ", langage.lang['OK']['sorted_double'].format(file=str(file), new_name=new, path=path), color=["Blue", None])

                    # For other errors
                    except OSError as error:
                        console1.printTerminal("❌: ", str(error), color=["Red", None])
                        log.error("❌: " + str(error))

    if conf.CONFIG['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):

            if str(file) not in notSort_userConfig and str(file) not in notSortList and str(file) not in check and str(file) != exe_file:

                try:
                    os.rename(str(file), './#Unsorted/'+str(file))
                    console1.printTerminal("✔: ", langage.lang['OK']['unsorted'].format(file=str(file)), color=["Purple", None])

                # For permission related errors
                except PermissionError:
                    console1.printTerminal("⚠: ", langage.lang['ERROR']['permission_file'].format(file=str(file)), color=["Orange", None])

                # For File Exists errors
                except FileExistsError:
                    new = duplicate(str(file), "./#Unsorted")
                    console1.printTerminal("✔: ", langage.lang['OK']['sorted_double_unsorted'].format(file=str(file), new_name=new), color=["Purple2", None])

                # For other errors
                except OSError as error:
                    console1.printTerminal("❌: ", str(error), color=["Red", None])
                    log.error("❌: " + str(error))
    del check
    button_tree.enable()

# ? TK ------------------------------------------------------------------------------->

def main():
    console1.show()
    button_tree.show()
    button_clear.show()
    button_option.show()
    button_option.enable()

    button_edit.hide()
    button_export.hide()
    button_import.hide()
    button_return.hide()
    button_moveToRoot.hide()
    button_deleteConfig.hide()

    ihm.hide()
    button_saveAndReturn.hide()

def option():
    console1.hide()
    button_tree.hide()
    button_clear.hide()
    button_option.show()
    button_option.disable()

    button_edit.show()
    button_export.show()
    button_import.show()
    button_return.show()
    button_moveToRoot.show()
    button_deleteConfig.show()

    ihm.hide()
    button_saveAndReturn.hide()

def edit():
    console1.hide()
    button_tree.hide()
    button_clear.hide()
    button_option.hide()
    

    button_edit.hide()
    button_export.hide()
    button_import.hide()
    button_return.hide()
    button_moveToRoot.hide()
    button_deleteConfig.hide()

    for i in ihm.tree.get_children():
        ihm.tree.delete(i)

    for key in conf.CONFIG['config_sort']:
        folder: str = conf.CONFIG['config_sort'][key]['path']
        extention: list = conf.CONFIG['config_sort'][key]['ext']

        ihm.tree.insert(parent='', index=END, text="", values=(key, folder, '|'.join(extention)))

    ihm.toggle_b.set_default_status(conf.CONFIG["unsorted"])
    doNotSort = "|".join(conf.CONFIG["doNotSort"])
    if not doNotSort == "":
        ihm.doNotSort_box.delete(0, END)
        ihm.doNotSort_box.insert(0, doNotSort)

    ihm.show()
    button_saveAndReturn.show()

# main window
window = Tk()
window.title("Tree")
window.iconbitmap(exe_path + "/img/tree.ico")
window.config(background='#202020')
window.geometry("600x600")
window.resizable(0, 0)
window.option_add("*font", 'Consolas 10 bold')

image = Image.open(exe_path + '/img/option.png')
image = image.resize((24, 24), Image.ANTIALIAS)
option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_up(window, text="lang : " + langage.get_locale(), bg='#202020', fg='#909090')
label_lang.posSize(x=259, y=570, width=82, height=32)
label_lang.show()

#VERSION
frame_version = Frame_up(window, bg='#202020')
frame_version.posSize(x=470, y=575, width=124, height=20)
frame_version.propagate(False)
frame_version.show()

last_version = update.get_version()

label_version = Button_up(frame_version, bg="#202020", fg="#990000", bd=0, highlightthickness=0, disabledforeground="#009900", state=DISABLED, text=version)

if last_version != None and last_version != version:
    label_version.config(activebackground="#202020", state=NORMAL, command=openWeb)

label_version.grid(row=0, column=1, pady=(1, 0))

label_version_text = Label_up(frame_version, text="version :", bg='#202020', fg='#909090')
label_version_text.grid(row=0, column=0, sticky=W)

#main
button_tree = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_sort'], command=lambda: Thread(target=sort).start())
button_tree.posSize(x=255, y=0, width=90, height=24)

button_clear = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_clear'], command=lambda: console1.clearTerminal())
button_clear.posSize(x=255, y=24, width=90, height=24)

button_option = Button_up(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=option)
button_option.posSize(x=2, y=574, width=24, height=24)

#option
button_edit = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_edit'], command=edit)
button_edit.posSize(x=217.5, y=24, width=165, height=24)

button_export = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_export'], command=conf.exportConfig)
button_export.posSize(x=217.5, y=48, width=165, height=24)

button_import = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_import'], command=conf.importConfig)
button_import.posSize(x=217.5, y=72, width=165, height=24)

button_moveToRoot = Button_up(window, bg="#555555", fg="#ff3030", activebackground="#555555", text="! "+"Move to root"+" !", command=moveToRoot)
button_moveToRoot.posSize(x=217.5, y=124, width=165, height=24)

button_deleteConfig = Button_up(window, bg="#555555", fg="#ff3030", activebackground="#555555", text="! "+"Delete config file"+" !", command=not_dev)
button_deleteConfig.posSize(x=217.5, y=148, width=165, height=24)

button_return = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_return'], command=main)
button_return.posSize(x=235, y=200, width=130, height=24)

#CONSOLE
colorConsole = {
    "Green": ["#000000", "#00ff00"],
    "Blue": ["#000000", "#26abff"],
    "Orange": ["#000000", "#ff7f00"],
    "Red": ["#000000", "#ff0000"],
    "Purple": ["#000000", "#ff0aff"],
    "Purple2": ["#000000", "#743DFF"]
}
console1 = Terminal_ScrolledText_up(window, bg="#000000", fg="#FFFFFF")
console1.configTag(colorConsole)
console1.posSize(x=0, y=48, width=600, height=524)

#tab config

ihm = Treeview_up(window, bg="#202020")
ihm.posSize(0, 0, 600, 500)
ihm.setColumns(("Name profile", "Folder", "Extention"), (150, 150, 300))
ihm.propagate(False)

def get_all_children():

    conf.CONFIG['config_sort'] = {}

    for line in ihm.tree.get_children():
        i = 0
        key = ""
        for value in ihm.tree.item(line)['values']:
                i += 1
                if i == 1:
                    conf.CONFIG['config_sort'][value] = {}
                    key = value
                if i == 2:
                    conf.CONFIG['config_sort'][key]['path'] = value
                if i == 3:
                    conf.CONFIG['config_sort'][key]['ext'] = value.split("|")

    conf.CONFIG["unsorted"] = ihm.toggle_b.get_status()
    doNotSort2 = ihm.doNotSort_box.get()
    if not doNotSort2 == "":
        conf.CONFIG["doNotSort"] = doNotSort2.split("|")
    else:
        conf.CONFIG["doNotSort"] = []

    conf.saveConfig()
    option()

button_saveAndReturn = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text="Return And Save", command=get_all_children)
button_saveAndReturn.posSize(x=2, y=574, width=130, height=24)

main()

window.mainloop()