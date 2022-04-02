import locale
from typing import TypedDict
from ruamel.yaml import YAML
from logger import Logger

LANG_AC = {
    "fr_FR": "Français",
    "en_EN": "English",
    None: "System"
}

class Lang_app:
    lang: TypedDict
    conf: TypedDict
    LANG_SYS: str
    log: Logger
    index: int

    def __init__(self, log: Logger, config: TypedDict, path: str = ".") -> None:
        self.log = log
        self.conf = config
        self.LANG_SYS: str = self.get_locale_ac()
        try:

            if config['lang'] != None:
                self.LANG_SYS = config["lang"]
                
            self.lang = self.__read_lang(f"{path}/lang/{self.LANG_SYS}.yml")
            self.log.info("Load Language")
        except:
            self.lang = self.__read_lang(f"{path}/lang/en_EN.yml")
            self.log.error("The system language did not charge")

        for index, key in enumerate(LANG_AC.keys()):
            if key == self.LANG_SYS:
                self.index = index
                break

    def reload_lang(self) -> None:
        if self.conf['lang'] != None:
                self.LANG_SYS = self.conf["lang"]
        self.lang = self.__read_lang()
        self.log.info("Reload lang")

    def __read_lang(self, path_file: str) -> TypedDict:

        with open(path_file, 'r', encoding='utf8') as file:

            classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)

        return classique_dict

    def get_locale_ac(self) -> str:
      return locale.getdefaultlocale()[0]

    def get_locale(self) -> str:
        return LANG_AC[self.LANG_SYS]

    def get_local_ac_from_name_lang(self, str:str) -> str:
        for key, value in LANG_AC.items():
            if value == str:
                return key
