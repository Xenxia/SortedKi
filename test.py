from tk_up.widgets import Button_up, Frame_up, Label_up, Tk_up, OptionMenu_up
from tk_up.managerThemes import ManagerThemes
from tk_up.managerWidgets import ManagerWidgets_up
from PyThreadUp import ThreadUP, ThreadManager
from Pylogger import Logger, DEBUG, INFO
from Pylang import Lang

lang = Lang(f"./lang")

def langSet(event):
    lang.setLang(lang.getLocaleShort(combox_option_lang.get()))
    print("lang")

def up(event):
    label_version_text["text"] = lang.t("UI.MAIN_MENU.lang")
    print("up")
    label_version_text.update()





window = Tk_up()

window.configWindows(title=f"test", geometry="700x700+center", iconbitmap=f"./img/icon.ico")

# window.iconbitmap()
# window.config(background='#202020')
# window.geometry("600x600")
window.resizable(0, 0)
# window.wm_attributes("-transparentcolor", "#123456")
# window.option_add("*font", 'Consolas 10 bold')
# window.columnconfigure(0, weight=1)
# window.rowconfigure(2, weight=1)

combox_option_lang = OptionMenu_up(window, default=0, list=lang.getLocalesLong(), justify='center')
combox_option_lang.current(lang.getIndexDefaultLang())
combox_option_lang.bind("<<ComboboxSelected>>", langSet)
combox_option_lang.gridPosSize(row=0, column=0, pady=(5,0)).show()

label_version = Button_up(window, text="reload", width=7, command=lambda: window.event_generate("<<TK_UP.Update>>"))
label_version.gridPosSize(row=1, column=0, pady=(0, 0)).show()

label_version_text = Label_up(window, text=lang.t("UI.MAIN_MENU.lang"))
label_version_text.gridPosSize(row=2, column=0).show()

window.event_add("<<TK_UP.Update>>", "test")
window.bind("<<TK_UP.Update>>", up)


print(window.event_info())

window.mainloop()