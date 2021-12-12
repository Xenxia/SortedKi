import locale
from typing import TypedDict
from ruamel.yaml import YAML

from logger import Logger

class Lang_app:
    lang: TypedDict
    LANG_SYS: str
    log: Logger

    def __init__(self, log: Logger, path: str = ".") -> None:
        self.log = log
        self.LANG_SYS: str = self.get_locale()
        try:
            self.lang = self.__read_lang(path +'/lang/'+self.LANG_SYS+'.yml')
            self.log.info("Load Lang")
        except:
            self.lang = self.__read_lang(path + '/lang/en_EN.yml')
            self.log.error("The system language did not charge")

    def reload_lang(self) -> None:
        self.lang = self.__read_lang()
        self.log.info("Reload lang")

    def __read_lang(self, path_file: str) -> TypedDict:

        with open(path_file, 'r', encoding='utf8') as file:

            classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)

        return classique_dict

    def get_locale(self) -> str:
      return locale.getdefaultlocale()[0]