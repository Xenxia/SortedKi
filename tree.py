#!/usr/bin/env python3

from ctypes import windll
import os, pathlib, sys, ntpath, shutil
from tkinter import *
from tkinter import filedialog
# from tkinter import ttk
from ImportPyinstaller import Pyimport
from PIL import Image, ImageTk

Pyimport(folder_path='func').add_path()
Pyimport(folder_path='lang').add_path()
Pyimport(folder_path='image').add_path()

exe_path = Pyimport().get_execute_path()

from conf import configTree
from ui import Button_v, Label_v, Terminal_v
from langages import lang_app

if Pyimport().is_compile:
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

def exports():
    pathfile = filedialog.asksaveasfilename(defaultextension=".configTree.yml" ,initialdir="./", title="Save config", filetypes=[("config file", "*.configTree.yml")])
    shutil.copy(src="./config.yml", dst=pathfile)

def imports():
    pathfile = filedialog.askopenfilename(initialdir="./", title="Import config", filetypes=[("config file", "*.configTree.yml")])
    os.remove("./config.yml")
    shutil.copy(src=pathfile, dst="./config.yml")
    windll.kernel32.SetFileAttributesW('./config.yml', 8198)
    conf.reloadConfig()

def sort():
    for key in conf.CONFIG[1]['config_sort']:
        for key2 in conf.CONFIG[1]['config_sort'][key]['ext']:
            path = './'+conf.CONFIG[1]['config_sort'][key]['path']

            if not os.path.exists(path):
                os.mkdir(path)

            for file in pathlib.Path('./').glob(key2):

                while True:

                    if str(file) in conf.CONFIG[1]['doNotSort'] or str(file) == exe_file or str(file) == "config.yml":
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

    if conf.CONFIG[1]['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):
            
            while True:

                if str(file) in conf.CONFIG[1]['doNotSort'] or str(file) == exe_file or str(file) == "config.yml":
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
    button_option.disable()

    button_edit.show()
    button_export.show()
    button_import.show()
    button_return.show()

def main():
    console1.show()
    button_tree.show()
    button_clear.show()
    button_option.enable()
    

    button_edit.hide()
    button_export.hide()
    button_import.hide()
    button_return.hide()

# main window
window = Tk()
window.title("Tree")
window.iconbitmap(exe_path + "/image/tree.ico")
window.config(background='#202020')
window.maxsize(600, 500)
window.minsize(600, 500)

image = Image.open(exe_path + '/image/option.png')
image = image.resize((22, 22), Image.ANTIALIAS)
option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_v(window, text="lang : " + langage.get_locale(), bg='#202020', fg='#909090')
label_lang.position(x=268, y=470, width=64, height=32)
label_lang.show()

#BUTTON
button_tree = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_sort'], command=sort)
button_tree.position(x=260, y=0, width=80, height=24)
button_tree.show()

button_clear = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_clear'], command=lambda: console1.clearTerminal())
button_clear.position(x=260, y=24, width=80, height=24)
button_clear.show()

button_option = Button_v(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=option)
button_option.position(x=2, y=474, width=24, height=24)
button_option.show()

button_edit = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_edit'])
button_edit.position(x=225, y=24, width=150, height=24)
button_edit.hide()

button_export = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_export'], command=exports)
button_export.position(x=225, y=48, width=150, height=24)
button_export.hide()

button_import = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_import'], command=imports)
button_import.position(x=225, y=72, width=150, height=24)
button_import.hide()

button_return = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_return'], command=main)
button_return.position(x=225, y=120, width=150, height=24)
button_return.hide()

#CONSOLE
console1 = Terminal_v(window, bg="#000000", fg="#FFFFFF")
console1.position(x=0, y=48, width=600, height=424)
console1.show()

#

window.mainloop()