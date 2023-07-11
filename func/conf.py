import os, stat, shutil, platform
from tkinter import filedialog
from typing import Any, TypedDict
from ruamel.yaml import YAML
from Pylogger import Logger

PLATFORM_SYS = platform.system()

if PLATFORM_SYS == "Windows":
    from ctypes import windll

class ConfigTree():
    log: Logger
    CONFIG: TypedDict
    CONFIG_FILE_NAME = "config.yml"
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
        "version_config_file": "2.0",
        "source": [],
        "unsorted": False,
        "doNotSort": [],
        "lang": None
    }

    def __init__(self, log: Logger, path_config: str = None) -> None:
        self.log = log


        if path_config is None:
            self.path_config = "./"
        else:
            self.path_config = f"{path_config}/{self.CONFIG_FILE_NAME}"

        if not os.path.exists(self.path_config):
            self.write_yaml(self.path_config, self.__DEFAULT_CONFIG)

            if PLATFORM_SYS == "Windows":
                windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)

            self.log.info("Create config")
            if not os.path.exists(self.path_config):
                self.log.error("Error during the creation of the sorting configuration file")

    def loadConfig(self) -> None:
        if os.path.exists(self.path_config):
            self.CONFIG = self.read_yaml(self.path_config)
            self.log.info("Load config")

    def saveConfig(self) -> None:
        if os.path.exists(self.path_config):
            self.write_yaml(self.path_config, self.CONFIG)
            self.log.info("Save config")


    def reloadConfig(self) -> None:
        self.CONFIG = None
        self.loadConfig()
        self.log.info("Reload config")

    def exportConfig(self) -> None:
        pathfile = filedialog.asksaveasfilename(defaultextension=".configTree.yml" ,initialdir="./", title="Save config", filetypes=[("config file", "*.configTree.yml")])
        if pathfile != '':
            shutil.copy(src=self.path_config, dst=pathfile)
            self.log.info("Exporting config")

    def importConfig(self) -> None:
        pathfile = filedialog.askopenfilename(initialdir="./", title="Import config", filetypes=[("config file", "*.configTree.yml")])
        if pathfile != '':
            if os.path.exists(self.path_config):
                os.remove(self.path_config)
            shutil.copy(src=pathfile, dst=self.path_config)

            if PLATFORM_SYS == "Windows":
                windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)

            self.reloadConfig()
            self.log.debug("Importing config")

    def write_yaml(self, name_file: str, content: Any) -> None:
        yml = YAML()
        yml.default_flow_style = None
        yml.width = 4096
        yml.indent(mapping=4, sequence=0, offset=0)

        if PLATFORM_SYS == "Windows":
            windll.kernel32.SetFileAttributesW(self.path_config, self.__SHOW_FILE)

        with open(name_file, 'w') as file:
            yml.dump(content, file)

        if PLATFORM_SYS == "Windows":
            windll.kernel32.SetFileAttributesW(self.path_config, self.__HIDE_FILE)
        
    def read_yaml(self, name_file: str) -> TypedDict:

        with open(name_file, 'r', encoding='utf8') as file:
            classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)

        return classique_dict

    def check_platform_rule(self, rule):

        path = rule["fullPath"]

        if path[0] == "/" and PLATFORM_SYS == "Linux":
            return True

        if path[0] == "/" and PLATFORM_SYS != "Linux":
            return False
        
        if path[1] == ":" and PLATFORM_SYS == "Windows":
            return True

        if path[1] == ":" and PLATFORM_SYS != "Windows":
            return False



