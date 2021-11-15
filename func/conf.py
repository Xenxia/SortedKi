from ctypes import windll
from typing import Any, Literal, Tuple, TypedDict
from collections import OrderedDict
from ruamel.yaml import YAML
import os

def write_yaml(name_file: str, content: Any) -> None:
    yml = YAML()
    yml.default_flow_style = False
    yml.width = 4096
    yml.indent(mapping=2, sequence=2, offset=2)
    with open(name_file, 'w') as file:
        yml.dump(content, file)
    
    file.close()

def read_yaml(name_file: str) -> Tuple[OrderedDict, TypedDict]:

    with open(name_file, 'r', encoding='utf8') as file:
        classique_dict: TypedDict = YAML(typ="safe", pure=True).load(file)
        file.close()

    with open(name_file, 'r', encoding='utf8') as file:
        OrderedDict_dict: OrderedDict = YAML().load(file)
        file.close()

    return OrderedDict_dict, classique_dict

def load_literal(literal: Literal) -> Any:
    return YAML().load(literal)

def write_default_config(lang):
    CONFIG_FILE_NAME = "config.yml"

    DEFAULT_CONFIG = """
    config_sort:

        exe:
            path: Executable
            ext: ['*.exe', '*.msi', '*.apk', '*.app', '*.gadget', '*.inf', '*.run', '*.vbs', '*.ws', '*.jar']

        doc:
            path: Document
            ext: ['*.xlsx', '*.docx', '*.pptx', '*.pdf']

        archive:
            path: Archive
            ext: ['*.7z', '*.rar', '*.zip', '*.tar', '*.iso', '*.sbx', '*.gz']

        music:
            path: Music
            ext: ['*.mp3', '*.ogg', '*.flac', '*.wav', '*.aac']

        picture:
            path: Image
            ext: ['*.png', '*.jpeg', '*.bmp', '*.tiff', '*.gif']

        video:
            path: Video
            ext: ['*.mp4', '*.mkv', '*.mka', '*.mks', '*.avi', '*.wmv', '*.flv', '*.mov']

    unsorted: false

    doNotSort: ['none']

    lang: none
    """

    write_yaml(CONFIG_FILE_NAME, load_literal(DEFAULT_CONFIG))
    windll.kernel32.SetFileAttributesW('./config.yml', 8198)
    if not os.path.exists(CONFIG_FILE_NAME):
        print(lang['ERROR']['create_config_file'])
        
