#!/usr/bin/env python3

from email.policy import default
import os, pathlib, sys, ntpath
from time import sleep
from tkinter import *
from tkinter import ttk
from ImportPyinstaller import Import_pyInst
from PyThreadUp import ThreadUP
from threading import Thread
from PIL import Image, ImageTk
import webbrowser

importPyInst = Import_pyInst()
importPyInst.add_path(folder_path='func')

VERSION = "1.0.0"
APP_NAME = "SortedTree"

notSortList = ["config.yml", "desktop.ini"]

exe_path = importPyInst.get_execute_path()

from update import Update
from conf import ConfigTree
from langages import LANG_AC, Lang_app
from logger import DEBUG, Logger
from ui import SCROLL_ALL, Button_up, Frame_up, Label_up, OptionMenu_up, Terminal_ScrolledText_up, Tk_up, Toggle_Button_up, Toplevel_up, Treeview_up, Widget_up

log = Logger(format="{time} | {levelname} : {msg}", levellog=DEBUG)
log.customize(level=("[", "]"))

if importPyInst.is_compiled:
    exe_file = os.path.realpath(sys.executable)
else:
    log.activColor(True)
    exe_file = os.path.realpath(__file__)

exe_file = ntpath.basename(exe_file)

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
    for file_path in pathlib.Path('./').rglob("*.*"):
        file_name = os.path.basename(file_path)
        os.rename(str(file_path), './'+str(file_name))
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

def notDev():
    console1.printTerminal("This feature is not developed", color=["Purple"])

def sort():

    button_tree.disable()

    notSort_userConfig = notSort()

    check: list = []

    for key in conf.CONFIG['config_sort']:
        for key2 in conf.CONFIG['config_sort'][key]['ext']:
            path = f"./{conf.CONFIG['config_sort'][key]['fullPath']}"

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

def mainUi():
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

#Option
def optionUi():
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

def fixLang(event):
    conf.CONFIG["lang"] = langage.get_local_ac_from_name_lang(combox_option_lang.get())
    conf.saveConfig()
    Thread(target=lambda: sendMessage(label_error_option, "#00ca00", langage.lang['UI']['OPTION_MENU']['message_change_lang'], 3)).start()

#Edit
def editUi():
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

    for i in ihm.treeView.tree.get_children():
        ihm.treeView.tree.delete(i)

    for key in conf.CONFIG['config_sort']:
        folder: str = conf.CONFIG['config_sort'][key]['folder']
        extention: list = conf.CONFIG['config_sort'][key]['ext']
        parent: str | None = conf.CONFIG['config_sort'][key]['parent']

        parent = parent if parent is not None else ''

        # ihm.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(extention)))
        ihm.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(extention)])

    ihm.toggle_b.set_default_status(conf.CONFIG["unsorted"])
    doNotSort = "|".join(conf.CONFIG["doNotSort"])
    if not doNotSort == "":
        ihm.doNotSort_box.delete(0, END)
        ihm.doNotSort_box.insert(0, doNotSort)

    ihm.show()
    button_saveAndReturn.show()

def unselect():
    try:
        ihm.edit.disable()
        ihm.remove.disable()
        ihm.unselect.disable()
        ihm.move_up.disable()
        ihm.move_down.disable()
        ihm.treeView.tree.selection_remove(ihm.treeView.tree.selection()[0])
    except:
        print("not select")

def delete():
    ihm.treeView.removeSelectedElement()
    unselect()

#Toplevel menu
def editMenu():

    addEditWindow.title(langage.lang['UI']['EDIT_MENU']['title_edit'])

    addOrEdit.config(text=langage.lang['UI']['EDIT_MENU']['button_apply'])

    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    addOrEdit.config(command=edit)

    try:
        selected = ihm.treeView.getSelectedElement()
        # values = self.treeView.tree.item(selected, 'values')

        # output to entry boxes
        name_box.insert(0, selected[0])
        id_box.insert(0, selected[1])
        topping_box.insert(0, selected[2])
        

        addEditWindow.show()

    except:
        print("not select")

def edit():
    try:
        selected = ihm.treeView.tree.selection()[0]
        ihm.treeView.tree.item(selected, text=name_box.get(), values=(id_box.get(), topping_box.get()))
        addEditWindow.hide()
    except:
        Thread(target=lambda: sendMessage(label_error_edit, "#ff3030", f"no items selected")).start()

def addMenu():
    addEditWindow.title(langage.lang['UI']['EDIT_MENU']['title_add'])

    addOrEdit.config(text=langage.lang['UI']['EDIT_MENU']['button_add'])

    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    addOrEdit.config(command=add)

    addEditWindow.show()

def add():
    name = name_box.get()
    id = id_box.get()
    topping = topping_box.get()

    sellect = ""

    try:
        sellect = ihm.treeView.tree.selection()[0]
    except:
        Thread(target=lambda: sendMessage(label_error_addEditWindow, "#ff3030", f"The profile {name} already exists")).start()

    if name!="" and id!="" and topping!="":
        ihm.treeView.tree.insert(parent=sellect, index=END, iid=name_box.get(), text=name_box.get(), values=(id_box.get(), topping_box.get()), tags=('evenrow',))
        unselect()
        addEditWindow.hide()
    else:
        print("box empty")

# main window
window = Tk_up()
window.configWindows(title=APP_NAME, geometry="600x600+center", iconbitmap=f"{exe_path}/img/tree.ico")
window.iconbitmap()
window.config(background='#202020')
window.geometry("600x600")
window.resizable(0, 0)
window.option_add("*font", 'Consolas 10 bold')
style = ttk.Style(window)

addEditWindow = Toplevel_up(window)
addEditWindow.geometry("600x95")
addEditWindow.iconbitmap(f"{exe_path}/img/tree.ico")
addEditWindow.config(background='#202020')
addEditWindow.resizable(0, 0)
addEditWindow.hide()

#Labels
nl = Label(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_name_profil'], bg="#202020", fg="#00ca00")
nl.grid(row=0, column=0, sticky=W)

il = Label(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_folder'], bg="#202020", fg="#00ca00")
il.grid(row=1, column=0, sticky=W)

tl = Label(addEditWindow, text=langage.lang['UI']['EDIT_MENU']['col_extention'], bg="#202020", fg="#00ca00")
tl.grid(row=2, column=0, sticky=W)

#Entry boxes
name_box = Entry(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
name_box.grid(row=0, column=1, sticky=W)

id_box = Entry(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
id_box.grid(row=1, column=1, sticky=W)

topping_box = Entry(addEditWindow, width=71, bg="#555555", fg="#FFFFFF")
topping_box.grid(row=2, column=1, sticky=W)

buttonF = Frame_up(addEditWindow)

addOrEdit = Button(buttonF, bg="#555555", fg="#00ca00", activebackground="#555555")
addOrEdit.grid(row=0, column=0)

cancel = Button(buttonF, text=langage.lang['UI']['EDIT_MENU']['button_cancel'], bg="#555555", fg="#00ca00", activebackground="#555555", command=addEditWindow.hide)
cancel.grid(row=0, column=1)

buttonF.grid(row=3, column=1, sticky=W)

#STYLE

window.option_add("*TCombobox*Listbox.background", "#323232")
window.option_add("*TCombobox*Listbox.foreground", "#00ca00")

style.theme_use("alt")
style.configure("Treeview", 
        background="#000000",
        foreground="#ffffff",
        rowheight=25,
        fieldbackground="#000000",
        indent=10,
        bd=1
        )

style.configure("Vertical.TScrollbar",
        background="#323232",
        arrowcolor="#ffffff",
        bordercolor="#000000",
        troughcolor='#252526',
        foreground="#ff0000"
        )

style.configure("Horizontal.TScrollbar",
        background="#323232",
        arrowcolor="#ffffff",
        bordercolor="#000000",
        troughcolor='#252526',
        foreground="#ff0000"
        )

style.configure("Treeview.Heading", 
        background="black", 
        foreground="white"
        )

style.configure("TCombobox", 
        background="#323232",
        arrowcolor="#ffffff",
        bordercolor="#000000",
        troughcolor='#252526',
        foreground="#00ca00",
        selectbackground="#555555",
        focusfill="#323232",
        fieldbackground="#323232",
        selectforeground="#00ca00",
        )

style.map("Vertical.TScrollbar", background=[('pressed', '#229922')])
style.map("Horizontal.TScrollbar", background=[('pressed', '#229922')])
style.map('Treeview.Heading', background=[('selected', '#000000')])
style.map('Treeview', background=[('selected', '#555555')])
style.map('TCombobox', 
    background=[('readonly', '#555555')], 
    fieldbackground=[('readonly', '#555555')],
    )

style.map('Listbox', 
    background=[('readonly', '#555555')], 
    fieldbackground=[('readonly', '#555555')],
    )

# custom indicator images
im_open = Image.open(exe_path + '/img/moins.png')
im_open = im_open.resize((15, 15), Image.ANTIALIAS)
im_close = Image.open(exe_path + '/img/plus.png')
im_close = im_close.resize((15, 15), Image.ANTIALIAS)
im_empty = Image.new('RGBA', (15, 15), '#00000000')

img_open = ImageTk.PhotoImage(im_open, name='img_open', master=window)
img_close = ImageTk.PhotoImage(im_close, name='img_close', master=window)
img_empty = ImageTk.PhotoImage(im_empty, name='img_empty', master=window)

# custom indicator
style.element_create('Treeitem.myindicator',
            'image', img_close, ('user1', '!user2', img_open), ('user2', img_empty),
            sticky='w', width=20)

# replace Treeitem.indicator by custom one
style.layout('Treeview.Item',
        [('Treeitem.padding',
        {'sticky': 'nswe',
        'children': [('Treeitem.myindicator', {'side': 'left', 'sticky': ''}),
            ('Treeitem.image', {'side': 'left', 'sticky': ''}),
            ('Treeitem.focus',
            {'side': 'left',
            'sticky': '',
            'children': [('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})]
        )

image = Image.open(exe_path + '/img/option.png')
image = image.resize((24, 24), Image.ANTIALIAS)
option_image = ImageTk.PhotoImage(image)

#LANG
label_lang = Label_up(window, text=f"{langage.lang['UI']['MAIN_MENU']['lang']} : {langage.get_locale_ac()}", bg='#202020', fg='#909090')
label_lang.posSize(x=238, y=570, width=124, height=32)
label_lang.show()

#LABEL ERROR
label_error_option = Label_up(window, text="", bg='#202020', fg='#202020')
label_error_option.posSize(x=0, y=270, width=600, height=32)

label_error_edit = Label_up(window, text="", bg='#202020', fg='#202020')
label_error_edit.posSize(x=0, y=410, width=600, height=32)

label_error_addEditWindow = Label_up(addEditWindow, text="", bg='#202020', fg='#ffffff')
label_error_addEditWindow.posSize(x=200, y=63, width=300, height=32)

#VERSION
frame_version = Frame_up(window, bg='#202020')
frame_version.posSize(x=470, y=575, width=124, height=20)
frame_version.propagate(False)
frame_version.show()

last_version = update.get_version()

label_version = Button_up(frame_version, bg="#202020", fg="#990000", bd=0, highlightthickness=0, disabledforeground="#009900", state=DISABLED, text=VERSION)

if last_version != None and last_version != VERSION:
    label_version.config(activebackground="#202020", state=NORMAL, command=openWeb)

label_version.grid(row=0, column=1, pady=(1, 0))

label_version_text = Label_up(frame_version, text="version :", bg='#202020', fg='#909090')
label_version_text.grid(row=0, column=0, sticky=W)

#main
button_tree = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_sort'], command=lambda: Thread(target=sort).start())
button_tree.posSize(x=255, y=0, width=90, height=24)

button_clear = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['MAIN_MENU']['button_clear'], command=lambda: console1.clearTerminal())
button_clear.posSize(x=255, y=24, width=90, height=24)

button_option = Button_up(window, bg="#202020", fg="#202020", bd=0, highlightthickness=0, activebackground="#202020", image=option_image, command=optionUi)
button_option.posSize(x=2, y=574, width=24, height=24)

#option
button_edit = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_edit'], command=editUi)
button_edit.posSize(x=210, y=24, width=180, height=24)

button_export = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_export'], command=export_conf)
button_export.posSize(x=210, y=48, width=180, height=24)

button_import = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_import'], command=import_conf)
button_import.posSize(x=210, y=72, width=180, height=24)

button_moveToRoot = Button_up(window, bg="#555555", fg="#ff3030", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_move_root'], command=moveToRoot)
button_moveToRoot.posSize(x=210, y=124, width=180, height=24)

button_deleteConfig = Button_up(window, bg="#555555", fg="#ff3030", wraplength=180, activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_delete_conf'], command=deletConfig)
button_deleteConfig.posSize(x=210, y=148, width=180)

combox_option_lang = OptionMenu_up(window, default=0, list=[LANG_AC[key] for key in LANG_AC.keys()], justify='center')
combox_option_lang.current(langage.index)
combox_option_lang.bind("<<ComboboxSelected>>", fixLang)
combox_option_lang.posSize(x=235, y=210,width=130, height=24)
combox_option_lang.show()

button_return = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['OPTION_MENU']['button_return'], command=mainUi)
button_return.posSize(x=235, y=250, width=130, height=24)

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

class IHM(Frame, Widget_up):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        Frame.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

        self.frameButton = Frame(self, bg="#202020")
        self.frameButton.grid(row=1, column=0, sticky=W)

        self.frameBox = Frame(self, bg="#202020", width=600)
        self.frameBox.grid(row=2, column=0, sticky=W)
        self.frameBox.propagate(False)
        
        self.treeView = Treeview_up(self, scroll=SCROLL_ALL, iid=True, child=True, show="tree headings", width=600, height=300)
        self.treeView.bind("<ButtonRelease-1>", self.selected)
        self.treeView.grid(row=0, column=0, sticky=W)

        self.unselect = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_unselect'], command=unselect, bg="#555555", fg="#00ca00", activebackground="#555555")
        self.unselect.grid(column=5, row=0, padx=5)
        self.unselect.disable()

        self.move_up = Button_up(self.frameButton, text="⬆", command=self.treeView.moveUpSelectedElement, bg="#555555", fg="#00ca00", activebackground="#555555")
        self.move_up.grid(column=4, row=0)
        self.move_up.disable()

        self.move_down = Button_up(self.frameButton, text="⬇", command=self.treeView.moveDownSelectedElement, bg="#555555", fg="#00ca00", activebackground="#555555")
        self.move_down.grid(column=3, row=0)
        self.move_down.disable()

        self.remove = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_delete'], command=delete, bg="#555555", fg="#00ca00", activebackground="#555555")
        self.remove.grid(column=2, row=0, padx=5)
        self.remove.disable()

        self.edit = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_edit'], command=editMenu, bg="#555555", fg="#00ca00", activebackground="#555555")
        self.edit.grid(column=1, row=0, padx=(5, 0))
        self.edit.disable()

        add = Button_up(self.frameButton, text=langage.lang['UI']['EDIT_MENU']['button_add'], command=addMenu, bg="#555555", fg="#00ca00", activebackground="#555555")
        add.grid(column=0, row=0)

        self.doNotSort_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
        self.doNotSort_box.grid(row=6, column=1, sticky=W, pady=(13, 0))

        d1 = Label(self.frameBox, text=langage.lang['UI']['EDIT_MENU']['label_not_sort'], bg="#202020", fg="#00ca00")
        d1.grid(row=6, column=0, pady=(20, 10), padx=(5, 5))

        self.toggle_b = Toggle_Button_up(self.frameBox, bg="#555555", activebackground="#555555", width=3)
        self.toggle_b.custom_toggle(("✔", "✖"))
        self.toggle_b.grid(column=1, row=7, sticky=W)

        u1 = Label(self.frameBox, text=langage.lang['UI']['EDIT_MENU']['label_unsorted'], bg="#202020", fg="#00ca00")
        u1.grid(row=7, column=0, padx=(5, 5))

        # event
    def selected(self, event):
        self.edit.enable()
        self.remove.enable()
        self.unselect.enable()
        self.move_up.enable()
        self.move_down.enable()

ihm = IHM(window, bg="#202020")
ihm.posSize(0, 0, 600, 450)
ihm.treeView.setColumns([
        langage.lang['UI']['EDIT_MENU']['col_name_profil'],
        langage.lang['UI']['EDIT_MENU']['col_folder'],
        langage.lang['UI']['EDIT_MENU']['col_extention']
    ], 
    [150, 150, 300]
)
ihm.propagate(False)

def getConfig():

    conf.CONFIG['config_sort'] = {}

    for iid in ihm.treeView.getAllChildren().items():
        key = ""
        fullPath = ""

        conf.CONFIG['config_sort'][iid[0]] = {}
        key = iid[0]

        value = iid[1]['values']
    
        conf.CONFIG['config_sort'][key]['parent'] = iid[1]['parent']
        conf.CONFIG['config_sort'][key]['folder'] = value[0]
        for index, parent in enumerate(ihm.treeView.getAllParentItem(key)[::-1]):

            folder = ihm.treeView.getItem(parent)["values"][0]
            
            if index != 0:
                fullPath += f"/{folder}"
            else:
                fullPath += f"{folder}"

        conf.CONFIG['config_sort'][key]['fullPath'] = fullPath
        conf.CONFIG['config_sort'][key]['ext'] = value[1].split("|")



    conf.CONFIG["unsorted"] = ihm.toggle_b.get_status()
    doNotSort2 = ihm.doNotSort_box.get()
    if not doNotSort2 == "":
        conf.CONFIG["doNotSort"] = doNotSort2.split("|")
    else:
        conf.CONFIG["doNotSort"] = []

    conf.saveConfig()
    optionUi()

button_saveAndReturn = Button_up(window, bg="#555555", fg="#00ca00", activebackground="#555555", text=langage.lang['UI']['EDIT_MENU']['buton_return_save'], command=getConfig)
button_saveAndReturn.posSize(x=2, y=574, width=180, height=24)

mainUi()
window.update()
window.mainloop()