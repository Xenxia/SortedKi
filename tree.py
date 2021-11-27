#!/usr/bin/env python3

import os, pathlib, sys, ntpath
from tkinter import *
# from tkinter import ttk
from ImportPyinstaller import Import_pyInst
from PIL import Image, ImageTk

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')
importPyInst.add_path(folder_path='lang')
importPyInst.add_path(folder_path='image')

version = "0.0.1b"

exe_path = importPyInst.get_execute_path()

from conf import configTree
from ui import Button_v, Label_v, Terminal_v, Treeview_v
from langages import lang_app

if importPyInst.is_compiled:
    exe_file = os.path.realpath(sys.executable)
else:
    exe_file = os.path.realpath(__file__)

exe_file = ntpath.basename(exe_file)

langage = lang_app(path=exe_path)

conf = configTree(lang=langage.lang)
conf.loadConfig()

def doublon(file: str, path: str) -> str:
    fileName, fileExt = os.path.splitext(file)

    num = 1
    while True:
        new_name = fileName+'_'+str(num)+fileExt
        new_path = path+'/'+new_name
        if not os.path.exists(new_path):
            os.rename(fileName+fileExt, new_path)
            break

        num += 1
    
    return new_name

def not_dev():
    console1.printTerminal(text="This feature is not developed", color="#FF0AFF", colored_text="*")

def sort():
    for key in conf.CONFIG['config_sort']:
        for key2 in conf.CONFIG['config_sort'][key]['ext']:
            path = './'+conf.CONFIG['config_sort'][key]['path']

            if not os.path.exists(path):
                os.mkdir(path)

            for file in pathlib.Path('./').glob(key2):

                while True:

                    if str(file) in conf.CONFIG['doNotSort'] or str(file) == exe_file or str(file) == "config.yml":
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
                        print('ERROR : ' + str(error))
                        break

    if conf.CONFIG['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):
            
            while True:

                if str(file) in conf.CONFIG['doNotSort'] or str(file) == exe_file or str(file) == "config.yml":
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
                    print('ERROR ' + str(error))
                    break

# ? TK ------------------------------------------------------------------------------->

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

    ihm.hide()
    button_saveAndReturn.hide()

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

    for i in ihm.tree.get_children():
        ihm.tree.delete(i)

    for key in conf.CONFIG['config_sort']:
        folder: str = conf.CONFIG['config_sort'][key]['path']
        extention: list = conf.CONFIG['config_sort'][key]['ext']

        ihm.tree.insert(parent='', index=END, text="", values=(key, folder, '|'.join(extention)))


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
label_lang = Label_v(window, text="lang : " + langage.get_locale(), bg='#202020', fg='#909090')
label_lang.position(x=259, y=570, width=82, height=32)
label_lang.show()

#VERSION
label_version = Label_v(window, text="version : " + version, bg='#202020', fg='#909090')
label_version.position(x=475, y=570, width=124, height=32)
label_version.show()

#BUTTON
button_tree = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_sort'], command=sort)
button_tree.position(x=255, y=0, width=90, height=24)

button_clear = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_clear'], command=lambda: console1.clearTerminal())
button_clear.position(x=255, y=24, width=90, height=24)

button_option = Button_v(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=option)
button_option.position(x=2, y=574, width=24, height=24)

button_edit = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_edit'], command=edit)
button_edit.position(x=217.5, y=24, width=165, height=24)

button_export = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_export'], command=conf.exportConfig)
button_export.position(x=217.5, y=48, width=165, height=24)

button_import = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_import'], command=conf.importConfig)
button_import.position(x=217.5, y=72, width=165, height=24)

button_return = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_return'], command=main)
button_return.position(x=235, y=120, width=130, height=24)

#CONSOLE
console1 = Terminal_v(window, bg="#000000", fg="#FFFFFF")
console1.position(x=0, y=48, width=600, height=524)

#tab config

ihm = Treeview_v(window, bg="#202020")
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
    
    print("save")
    conf.saveConfig()
    option()



button_saveAndReturn = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text="Return And Save", command=get_all_children)
button_saveAndReturn.position(x=2, y=574, width=130, height=24)

main()

window.mainloop()