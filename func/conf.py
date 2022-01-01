from ctypes import windll
from tkinter import filedialog
from typing import Any, TypedDict
from ruamel.yaml import YAML
import os, stat, shutil

from logger import Logger

class ConfigTree():
    log: Logger
    CONFIG: TypedDict
    CONFIG_FILE_NAME = "config.yml"
    __HIDE_FILE: int = stat.FILE_ATTRIBUTE_HIDDEN+stat.FILE_ATTRIBUTE_SYSTEM
    __SHOW_FILE: int = stat.FILE_ATTRIBUTE_NORMAL
    __DEFAULT_CONFIG = {
        "config_sort":{
            "Runtime":{
                "parent": None,
                "folder": "Runtime",
                "fullPath": "Runtime",
                "ext":['*.exe', '*.msi', '*.apk', '*.app', '*.gadget', '*.inf', '*.run', '*.vbs', '*.ws', '*.jar']
            },
            "Document":{
                "parent": None,
                "folder": "Document",
                "fullPath": "Document",
                "ext":['*.xlsx', '*.docx', '*.pptx', '*.pdf']
            },
            "Archive":{
                "parent": None,
                "folder": "Archive",
                "fullPath": "Archive",
                "ext":['*.7z', '*.rar', '*.zip', '*.tar', '*.iso', '*.sbx', '*.gz']
            },
            "Music":{
                "parent": None,
                "folder": "Music",
                "fullPath": "Music",
                "ext":['*.mp3', '*.ogg', '*.flac', '*.wav', '*.aac']
            },
            "Picture":{
                "parent": None,
                "folder": "Picture",
                "fullPath": "Picture",
                "ext":['*.png', '*.jpeg', '*.jpg','*.bmp', '*.tiff', '*.gif']
            },
            "Video":{
                "parent": None,
                "folder": "Video",
                "fullPath": "Video",
                "ext":['*.mp4', '*.mkv', '*.mka', '*.mks', '*.avi', '*.wmv', '*.flv', '*.mov']
            },
        },
        "unsorted": False,
        "doNotSort": [],
        "lang": None
    }

    def __init__(self, log: Logger) -> None:
        self.log = log
        if not os.path.exists(self.CONFIG_FILE_NAME):
            self.write_yaml(self.CONFIG_FILE_NAME, self.__DEFAULT_CONFIG)
            windll.kernel32.SetFileAttributesW(self.CONFIG_FILE_NAME, self.__HIDE_FILE)
            self.log.info("Create config")
            if not os.path.exists(self.CONFIG_FILE_NAME):
                self.log.error("Error during the creation of the sorting configuration file")

    def loadConfig(self) -> None:
        if os.path.exists(self.CONFIG_FILE_NAME):
            self.CONFIG = self.read_yaml(self.CONFIG_FILE_NAME)
            self.log.info("Load config")

    def saveConfig(self) -> None:
        if os.path.exists(self.CONFIG_FILE_NAME):
            self.write_yaml(self.CONFIG_FILE_NAME, self.CONFIG)
            self.log.info("Save config")


    def reloadConfig(self) -> None:
        self.CONFIG = None
        self.loadConfig()
        self.log.info("Reload config")

    def exportConfig(self) -> None:
        pathfile = filedialog.asksaveasfilename(defaultextension=".configTree.yml" ,initialdir="./", title="Save config", filetypes=[("config file", "*.configTree.yml")])
        if pathfile != '':
            shutil.copy(src=self.CONFIG_FILE_NAME, dst=pathfile)
            self.log.info("Exporting config")

    def importConfig(self) -> None:
        pathfile = filedialog.askopenfilename(initialdir="./", title="Import config", filetypes=[("config file", "*.configTree.yml")])
        if pathfile != '':
            if os.path.exists(self.CONFIG_FILE_NAME):
                os.remove(self.CONFIG_FILE_NAME)
            shutil.copy(src=pathfile, dst=self.CONFIG_FILE_NAME)
            windll.kernel32.SetFileAttributesW(self.CONFIG_FILE_NAME, self.__HIDE_FILE)
            self.reloadConfig()
            self.log.debug("Importing config")

    def write_yaml(self, name_file: str, content: Any) -> None:
        yml = YAML()
        yml.default_flow_style = None
        yml.width = 4096
        yml.indent(mapping=4, sequence=0, offset=0)

        windll.kernel32.SetFileAttributesW(self.CONFIG_FILE_NAME, self.__SHOW_FILE)

        with open(name_file, 'w') as file:
            yml.dump(content, file)

        windll.kernel32.SetFileAttributesW(self.CONFIG_FILE_NAME, self.__HIDE_FILE)
        
    def read_yaml(self, name_file: str) -> TypedDict:

        with open(name_file, 'r', encoding='utf8') as file:
            classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)

        return classique_dict

    # def __load_literal(self, literal: Literal) -> Any:
    #     return YAML().load(literal)

