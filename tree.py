#!/usr/bin/env python3

import os, pathlib, sys, ntpath
from tkinter import *
# from tkinter import ttk
from ImportPyinstaller import Import_pyInst
from PIL import Image, ImageTk
import webbrowser

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='lang')
importPyInst.add_path(folder_path='image')

version = "0.0.2b"

exe_path = importPyInst.get_execute_path()

from conf import ConfigTree
from ui import Button_x, Frame_x, Label_x, Terminal_x, Treeview_x
from logger import INFO, Logger
from langages import Lang_app
from update import Update

log = Logger(format="{time} | {levelname} : {msg}", levellog=INFO)
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

def doublon(file: str, path: str) -> str:

    fileName, fileExt = os.path.splitext(file)

    numWhile: int = 0
    while True:
        if numWhile != 0:
            new_name = new_name.replace(new_name[-2:], "_"+str(numWhile))
        else:
            if fileName[-2]!="_":
                new_name = fileName+'_'+str(numWhile)
            else:
                new_name = fileName.replace(fileName[-2:], "_"+str(numWhile+1))

        new_path = path+'/'+new_name+fileExt
        if not os.path.exists(new_path):
            os.rename(fileName+fileExt, new_path)
            break
        numWhile += 1
    return new_name

def not_dev():
    console1.printTerminal(text="This feature is not developed", color="#FF0AFF", colored_text="*")

def sort():

    doNotSort_l = notSort()

    for key in conf.CONFIG['config_sort']:
        for key2 in conf.CONFIG['config_sort'][key]['ext']:
            path = './'+conf.CONFIG['config_sort'][key]['path']

            if not os.path.exists(path):
                os.mkdir(path)

            for file in pathlib.Path('./').glob(key2):

                while True:

                    if str(file) in doNotSort_l or str(file) == exe_file or str(file) == "config.yml":
                        break

                    try:
                        os.rename(str(file), path+'/'+str(file))
                        console1.printTerminal("OK: " + langage.lang['OK']['sorted'].format(file=str(file), path=path), color='#00FF00', colored_text='OK')
                        break

                    # For permission related errors
                    except PermissionError:
                        console1.printTerminal("WARNING: " + langage.lang['ERROR']['permission_file'].format(file=str(file)), color="#FF7F00", colored_text="WARNING")
                        break

                    except FileExistsError:
                        new = doublon(str(file), path)
                        console1.printTerminal("OK: " + langage.lang['OK']['sorted_double'].format(file=str(file), new_name=new, path=path), color='#00FF00', colored_text='OK')
                        break

                    # For other errors
                    except OSError as error:
                        console1.printTerminal('ERROR : ' + str(error), color="#FF0000", colored_text="ERROR")
                        log.error('ERROR : ' + str(error))
                        break

    if conf.CONFIG['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):
            
            while True:

                if str(file) in doNotSort_l or str(file) == exe_file or str(file) == "config.yml":
                    break

                try:
                    os.rename(str(file), './#Unsorted/'+str(file))
                    console1.printTerminal("OK: " + langage.lang['OK']['unsorted'].format(file=str(file), path="./#Unsorted"), color='#00FF00', colored_text='OK')
                    break

                # For permission related errors
                except PermissionError:
                    console1.printTerminal("WARNING: " + langage.lang['ERROR']['permission_file'].format(file=str(file)), color="#FF7F00", colored_text="WARNING")
                    break

                except FileExistsError:
                    new = doublon(str(file), path)
                    console1.printTerminal("OK: " + langage.lang['OK']['sorted_double'].format(file=str(file), new_name=new, path=path), color='#00FF00', colored_text='OK')
                    break

                # For other errors
                except OSError as error:
                    log.error('ERROR ' + str(error))
                    break

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
window.iconbitmap(exe_path + "/image/tree.ico")
window.config(background='#202020')
window.geometry("600x600")
window.resizable(0, 0)
window.option_add("*font", 'Consolas 10 bold')

image = Image.open(exe_path + '/image/option.png')
image = image.resize((22, 22), Image.ANTIALIAS)
option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_x(window, text="lang : " + langage.get_locale(), bg='#202020', fg='#909090')
label_lang.position(x=259, y=570, width=82, height=32)
label_lang.show()

#VERSION
frame_version = Frame_x(window, bg='#202020')
frame_version.position(x=470, y=575, width=124, height=20)
frame_version.propagate(False)
frame_version.show()

last_version = update.get_version()

label_version = Button_x(frame_version, bg="#202020", fg="#990000", bd=0, highlightthickness=0, disabledforeground="#009900", state=DISABLED, text=version)

if last_version != None and last_version != version:
    label_version.config(activebackground="#202020", state=NORMAL, command=openWeb)

label_version.grid(row=0, column=1, pady=(1, 0))

label_version_text = Label_x(frame_version, text="version :", bg='#202020', fg='#909090')
label_version_text.grid(row=0, column=0, sticky=W)

#BUTTON
button_tree = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_sort'], command=sort)
button_tree.position(x=255, y=0, width=90, height=24)

button_clear = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_clear'], command=lambda: console1.clearTerminal())
button_clear.position(x=255, y=24, width=90, height=24)

button_option = Button_x(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=option)
button_option.position(x=2, y=574, width=24, height=24)

#option
button_edit = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_edit'], command=edit)
button_edit.position(x=217.5, y=24, width=165, height=24)

button_export = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_export'], command=conf.exportConfig)
button_export.position(x=217.5, y=48, width=165, height=24)

button_import = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_import'], command=conf.importConfig)
button_import.position(x=217.5, y=72, width=165, height=24)

button_moveToRoot = Button_x(window, bg="#555555", fg="#ff3030", activebackground="#555555", text="! "+"Move to root"+" !", command=moveToRoot)
button_moveToRoot.position(x=217.5, y=124, width=165, height=24)

button_deleteConfig = Button_x(window, bg="#555555", fg="#ff3030", activebackground="#555555", text="! "+"Delete config file"+" !", command=not_dev)
button_deleteConfig.position(x=217.5, y=148, width=165, height=24)

button_return = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_return'], command=main)
button_return.position(x=235, y=200, width=130, height=24)

#CONSOLE
console1 = Terminal_x(window, bg="#000000", fg="#FFFFFF")
console1.position(x=0, y=48, width=600, height=524)

#tab config

ihm = Treeview_x(window, bg="#202020")
ihm.position(0, 0, 600, 500)
ihm.setColumns(("Name profile", "Folder", "Extention"))
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



button_saveAndReturn = Button_x(window, bg="#555555", fg="#00ca00", activebackground="#555555", text="Return And Save", command=get_all_children)
button_saveAndReturn.position(x=2, y=574, width=130, height=24)

main()

window.mainloop()