import locale
from typing import TypedDict
from ruamel.yaml import YAML

class lang_app:
    lang: TypedDict
    LANG_SYS: str

    def __init__(self, path: str = ".") -> None:
        self.LANG_SYS: str = self.get_locale()
        try:
            self.lang = self.__read_lang(path +'/lang/'+self.LANG_SYS+'.yml')
            print("INFO : load lang")
        except:
            self.lang = self.__read_lang(path + '/lang/en_EN.yml')

    def reload_lang(self) -> None:
        self.lang = self.__read_lang()

    def __read_lang(self, path_file: str) -> TypedDict:

        with open(path_file, 'r', encoding='utf8') as file:

            classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)

        file.close()

        return classique_dict

    def get_locale(self) -> str:
      return locale.getdefaultlocale()[0]