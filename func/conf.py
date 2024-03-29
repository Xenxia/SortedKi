import os, stat, shutil, platform, json
from tkinter import filedialog
from typing import Any, TypedDict
from Pylogger import Logger

PLATFORM_SYS = platform.system()

if PLATFORM_SYS == "Windows":
    from ctypes import windll

class Config_():
    log: Logger
    CONFIG: TypedDict
    CONFIG_FILE_NAME = "config.json"
    CONFIG_VERSION = "3.0"
    CONFIG_EXT = ".confki.json"
    __SYS_WINDOWS: bool = (PLATFORM_SYS == "Windows")
    __SYS_LINUX: bool = (PLATFORM_SYS == "Linux")

    __HIDE_FILE: int = stat.FILE_ATTRIBUTE_HIDDEN+stat.FILE_ATTRIBUTE_SYSTEM
    __SHOW_FILE: int = stat.FILE_ATTRIBUTE_NORMAL
    __DEFAULT_CONFIG = {
        "config_sort":{
            "Runtime":{
                "disable": False,
                "parent": None,
                "folder": "Runtime",
                "fullPath": "Runtime",
                "rule":['*.exe', '*.msi', '*.apk', '*.app', '*.gadget', '*.inf', '*.run', '*.vbs', '*.ws', '*.jar'],
                "pathStatic": False,
            },
            "Document":{
                "disable": False,
                "parent": None,
                "folder": "Document",
                "fullPath": "Document",
                "rule":['*.xlsx', '*.docx', '*.pptx', '*.pdf'],
                "pathStatic": False,
            },
            "Archive":{
                "disable": False,
                "parent": None,
                "folder": "Archive",
                "fullPath": "Archive",
                "rule":['*.7z', '*.rar', '*.zip', '*.tar', '*.iso', '*.sbx', '*.gz'],
                "pathStatic": False,
            },
            "Music":{
                "disable": False,
                "parent": None,
                "folder": "Music",
                "fullPath": "Music",
                "rule":['*.mp3', '*.ogg', '*.flac', '*.wav', '*.aac'],
                "pathStatic": False,
            },
            "Picture":{
                "disable": False,
                "parent": None,
                "folder": "Picture",
                "fullPath": "Picture",
                "rule":['*.png', '*.jpeg', '*.jpg','*.bmp', '*.tiff', '*.gif'],
                "pathStatic": False,
            },
            "Video":{
                "disable": False,
                "parent": None,
                "folder": "Video",
                "fullPath": "Video",
                "rule":['*.mp4', '*.mkv', '*.mka', '*.mks', '*.avi', '*.wmv', '*.flv', '*.mov'],
                "pathStatic": False,
            },
        },
        "sources": {
            "Root" : {
                "path": ".", 
                "disable": False
            }
        },
        "version_config_file": f"{CONFIG_VERSION}",
        "unsorted": False,
        "sorting_exception": [],
        "lang": None
    }

    def __init__(self, log: Logger, path_config: str = None) -> None:
        self.log = log


        if path_config is None:
            self.path_config = "./"
        else:
            self.path_config = f"{path_config}/{self.CONFIG_FILE_NAME}"

        if not os.path.exists(self.path_config):
            self.write_conf(self.path_config, self.__DEFAULT_CONFIG)

            if self.__SYS_WINDOWS:
                windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)

            self.log.info("Create config")
            if not os.path.exists(self.path_config):
                self.log.error("Error during the creation of the sorting configuration file")

    def loadConfig(self) -> None:
        if os.path.exists(self.path_config):
            self.CONFIG = self.read_conf(self.path_config)
            self.log.info("Load config")

    def saveConfig(self) -> None:
        if os.path.exists(self.path_config):
            self.write_conf(self.path_config, self.CONFIG)
            self.log.info("Save config")

    def reloadConfig(self) -> None:
        self.CONFIG = None
        self.loadConfig()
        self.log.info("Reload config")

    def exportConfig(self) -> bool:
        pathfile = filedialog.asksaveasfilename(defaultextension=self.CONFIG_EXT ,initialdir="./", title="Save config", filetypes=[("config file", f"*{self.CONFIG_EXT}")])

        self.log.debug(pathfile)
        if pathfile != '':
            shutil.copy(src=self.path_config, dst=pathfile)
            self.log.info("Exporting config")
            return True

        return False

    def importConfig(self) -> bool:
        pathfile = filedialog.askopenfilename(initialdir="./", title="Import config", filetypes=[("config file", f"*{self.CONFIG_EXT}")])

        self.log.debug(pathfile)

        if pathfile != '':
            if os.path.exists(self.path_config):
                os.remove(self.path_config)
            shutil.copy(src=pathfile, dst=self.path_config)

            if self.__SYS_WINDOWS: windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)

            self.reloadConfig()
            self.log.debug("Importing config")
            return True
    
        return False

    def write_conf(self, name_file: str, content: Any) -> None:

        if self.__SYS_WINDOWS: windll.kernel32.SetFileAttributesW(self.path_config, self.__SHOW_FILE)

        with open(name_file, 'w') as file:
            json.dump(content, file, indent=4, )

        if self.__SYS_WINDOWS:
            windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)
        
    def read_conf(self, name_file: str) -> TypedDict:

        with open(name_file, 'r', encoding='utf8') as file:
            classique_dict: TypedDict = json.load(file)

        return classique_dict

    def check_platform_rule(self, rule):

        path = rule["fullPath"]

        if path[0] == "/" and self.__SYS_LINUX:
            return True

        if path[0] == "/" and not self.__SYS_LINUX:
            return False
        
        if path[1] == ":" and self.__SYS_WINDOWS:
            return True

        if path[1] == ":" and not self.__SYS_WINDOWS:
            return False
        
    def delete(self):
        os.remove(self.path_config)



