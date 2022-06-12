import locale
from typing import TypedDict
from ruamel.yaml import YAML
from func.logger import Logger

LANG_AC: dict[str, list] = {
    "Français": ["fr_FR"],
    "English": ["en_EN"],
    "System": [None]
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
        self.index = len(LANG_AC)-1
        try:
            if config['lang'] != None:
                self.LANG_SYS = config["lang"]
                
            self.lang = self.__read_lang(f"{path}/lang/{self.LANG_SYS}.yml")
            self.log.info("Load Language")
            for index, key in enumerate(LANG_AC.keys()):
                if LANG_AC[key][0] == self.LANG_SYS:
                    self.index = index
                    break
        except:
            self.lang = self.__read_lang(f"{path}/lang/en_EN.yml")
            self.log.error("The system language did not charge")

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

        for local, list_ac in LANG_AC.items():
            if self.LANG_SYS in list_ac:
                return local
            else:
                return "System"

    def get_local_ac_from_name_lang(self, str:str) -> str:
        return LANG_AC[str][0]
