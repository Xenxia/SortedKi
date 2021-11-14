#!/usr/bin/env python3

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

from conf import read_yaml, write_default_config
from ui import Button_v, Label_v, Text_v
from langages import lang_app

if Pyimport().is_compile:
    exe_file = os.path.realpath(sys.executable)
else:
    exe_file = os.path.realpath(__file__)

exe_file = ntpath.basename(exe_file)

# sys.exit()

langage = lang_app(path=exe_path)

if not os.path.exists('config.yml'):
    write_default_config(langage.lang)
    dico = read_yaml('config.yml')
else:
    dico = read_yaml('config.yml')

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

def ctrlEvent(event) -> str:
    if(12==event.state and event.keysym=='c' ):
        return
    else:
        return "break"

def printTerminal(text: str, terminal: Text, colored_text: str = 'none', color: str = '#FFFFFF') -> None:
    terminal.insert(END, text + "\n")
    terminal.see(END)
    terminal.tag_config(color, background="#000000", foreground=color)
    if color != 'none':
        if colored_text == '*':
            colored_text = text
        pos = '1.0'
        while True:
            idx = terminal.search(colored_text, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(colored_text))
            terminal.tag_add(color, idx, pos)

def not_dev(terminal: Text):
    printTerminal(text="This feature is not developed", terminal=terminal, color="#FF0AFF", colored_text="*")

def clearTerminal(terminal: Text) -> None:
    terminal.delete("1.0","end")

def export():
    pathfile = filedialog.asksaveasfilename(defaultextension=".configTree" ,initialdir="./", title="Save config", filetypes=[("config file", "*.configTree")])
    shutil.copy(src="./config.yml", dst=pathfile)

def sort():
    for key in dico[1]['config_sort']:
        for key2 in dico[1]['config_sort'][key]['ext']:
            path = './'+dico[1]['config_sort'][key]['path']
            
            if not os.path.exists(path):
                os.mkdir(path)

            for file in pathlib.Path('./').glob(key2):

                while True:

                    if str(file) in dico[1]['doNotSort'] or str(file) == exe_file:
                        break

                    try:
                        os.rename(str(file), path+'/'+str(file))

                    # For permission related errors
                    except PermissionError:
                        printTerminal("WARNING: " + langage.lang['ERROR']['permission_file'].format(file=str(file)), console1, color="#FF7F00", colored_text="WARNING")
                        break

                    except FileExistsError:
                        new = doublon(str(file), path)
                        printTerminal("OK: " + langage.lang['OK']['sorted_double'].format(file=str(file), new_name=new, path=path), console1, color='#00FF00', colored_text='OK')
                        break

                    # For other errors
                    except OSError as error:
                        printTerminal('ERROR : ' + str(error), console1, color="#FF0000", colored_text="ERROR")
                        print('ERROR : ' + str(error))
                        break

                    printTerminal("OK: " + langage.lang['OK']['sorted'].format(file=str(file), path=path), console1, color='#00FF00', colored_text='OK')
                    break

    if dico[1]['unsorted'] == True :
        if not os.path.exists('./#Unsorted'):
            os.mkdir('./#Unsorted')
        
        for file in pathlib.Path('./').glob('*.*'):
            
            while True:

                if str(file) in dico[1]['doNotSort'] or str(file) == exe_file:
                    break

                try:
                    os.rename(str(file), './#Unsorted/'+str(file))
                    break

                # For permission related errors
                except PermissionError:
                    input(langage.lang['ERROR']['permission_file'].format(file=str(file)))

                except FileExistsError:
                    doublon(str(file), path)
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
label_lang = Label_v(window, text="lang : " + langage.get_local_lang(), bg='#202020', fg='#909090')
label_lang.conf_pos(x=268, y=470, width=64, height=32)
label_lang.show()

#BUTTON
button_tree = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_sort'], command=sort)
button_tree.conf_pos(x=260, y=0, width=80, height=24)
button_tree.show()

button_clear = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_clear'], command=lambda: clearTerminal(console1))
button_clear.conf_pos(x=260, y=24, width=80, height=24)
button_clear.show()

button_option = Button_v(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=option)
button_option.conf_pos(x=2, y=474, width=24, height=24)
button_option.show()

button_edit = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_edit'])
button_edit.conf_pos(x=225, y=24, width=150, height=24)
button_edit.hide()

button_export = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_export'], command=export)
button_export.conf_pos(x=225, y=48, width=150, height=24)
button_export.hide()

button_import = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_import'])
button_import.conf_pos(x=225, y=72, width=150, height=24)
button_import.hide()

button_return = Button_v(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['button_return'], command=main)
button_return.conf_pos(x=225, y=120, width=150, height=24)
button_return.hide()

#CONSOLE
console1 = Text_v(window, bg="#000000", fg="#FFFFFF")
console1.bind("<Key>", lambda e: ctrlEvent(e))
console1.conf_pos(x=0, y=48, width=600, height=424)
console1.show()

# console1.place_forget()

window.mainloop()