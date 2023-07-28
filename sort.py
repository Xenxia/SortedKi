import ntpath
import os
import pathlib
import shutil
from Pylogger import Logger
from Pylang import Lang

from func.conf import Config_

#Page
from page.main import main

NOT_SORT_LIST = ["config.json", "desktop.ini", "debug.log"]
NAME_FOLDER_UNSORTED = "#_"

class Sorting:

    log: Logger
    conf: Config_
    checkedFile: list

    def __init__(self, log: Logger, lang: Lang, conf: Config_, pathDirExe: str, nameAppExe:str, mSort: main) -> None:
        self.log = log
        self.conf = conf
        self.checkedFile = []
        self.nameAppExe = nameAppExe
        self.pathDirExe = pathDirExe
        self.parentPath = pathDirExe
        self.searchPath = pathDirExe
        self.console = mSort.console1
        self.langage = lang

    def start(self):

        dontSortFileRule = self.__dontSortFiles()

        self.log.debug(f"dontSortFileRule : {dontSortFileRule}", "Sorting-start")

        self.checkedFile = []

        for profileName in self.conf.CONFIG['config_sort']:

            disable = self.conf.CONFIG['config_sort'][profileName]['disable']

            for rule in self.conf.CONFIG['config_sort'][profileName]['rule']:
                fullPathConfig: str = self.conf.CONFIG['config_sort'][profileName]['fullPath']
                pathStatic: bool = self.conf.CONFIG['config_sort'][profileName]['pathStatic']

                if pathStatic:

                    if not os.path.exists(f"{fullPathConfig}"):
                        self.log.debug("Create static Dir : " + f"{fullPathConfig}", "Sorting-start")
                        os.makedirs(f"{fullPathConfig}", exist_ok=True)
                else:

                    if not os.path.exists(f"{self.parentPath}/{fullPathConfig}"):
                        self.log.debug("Create Dir : " + f"{self.parentPath}/{fullPathConfig}", "Sorting-start")
                        os.makedirs(f"{self.parentPath}/{fullPathConfig}", exist_ok=True)

                if rule == "":
                    break

                for key, value in self.conf.CONFIG['sources'].items():

                    if value["disable"]:
                        continue

                    if key == "Root":
                        source = self.searchPath
                    else:
                        source = value["path"]

                    self.log.debug(f"Source : {source}")

                    self.sort(rule, dontSortFileRule, fullPathConfig, source, pathStatic, disable)

        if self.conf.CONFIG['unsorted'] == True :
            if not os.path.exists(f"{self.pathDirExe}/{NAME_FOLDER_UNSORTED}"):
                self.log.debug("Create Unsorted Dir")
                os.mkdir(f"{self.pathDirExe}/{NAME_FOLDER_UNSORTED}")

            for key, value in self.conf.CONFIG['sources'].items():

                if value["disable"]:
                        continue

                if key == "Root":
                    source = self.searchPath
                else:
                    source = value["path"]

                self.unsorted(dontSortFileRule, source)


    def sort(self, rule: str, dontSortFileRule: list, fullPathConfig: str, source: str, staticPath: bool, disableRule: bool):

        self.log.debug(f"Start sort - rule {rule}")

        for pathFile in pathlib.Path(source).glob(rule):

            nameFile = pathFile.name

            parentPath = f"{self.pathDirExe}/{fullPathConfig}"
            futurPathFile = f"{parentPath}/{nameFile}"

            if staticPath:
                parentPath = f"{fullPathConfig}"
                futurPathFile = f"{fullPathConfig}/{nameFile}"

            duplica = False
            sort = False
            permission = False
            new = "new"
            err = [False, "none"]

            if str(nameFile) not in dontSortFileRule and str(nameFile) not in NOT_SORT_LIST and str(nameFile) != self.nameAppExe:

                self.log.debug(f"name file : {nameFile}", "sort")

                self.checkedFile.append(str(nameFile))

                if disableRule:
                    continue

                if not os.path.exists(futurPathFile):

                    try:
                        if os.path.isfile(pathFile.as_posix()):

                            with open(pathFile.as_posix(), "a", encoding="utf8") as file:
                                file.close()

                            shutil.move(pathFile.as_posix(), futurPathFile)
                            self.log.debug("OK", "sort")
                            sort = True
                        else:
                            self.log.debug(f"Not file {str(nameFile)}", "sort")
                            break

                    # For permission related errors
                    except PermissionError:
                        self.log.error("Permission error", "sort")
                        permission = True

                    # For other errors
                    except ValueError as error:
                        self.log.error(f"OS error - {error}", "sort")
                        err = [True, error]

                else:
                    try:
                        if os.path.isfile(pathFile.as_posix()):
                            self.log.debug(f"Duplicate {nameFile}", "sort")
                            new = self.duplicate(str(nameFile), f"{parentPath}")

                            with open(pathFile.as_posix(), "a", encoding="utf8") as file:
                                file.close()
                            
                            shutil.move(src = pathFile.as_posix(), dst = f"{parentPath}/{new}")
                            sort, duplica = True, True
                        else:
                            break

                    except PermissionError:
                        self.log.error("Permission Duplicate error", "sort")
                        permission = True
                        
                    # For other errors
                    except OSError as error:
                        self.log.error(f"Duplicate - {error}", "sort")
                        err = [True, error]

            if sort and not duplica:
                self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('TERM.move'), f" {str(fullPathConfig)}", color=["Green", "Bold", None, "Bold"])

            if sort and duplica:
                self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('TERM.rename'), f" {str(new)} ", self.langage.t('TERM.move'), f" {str(fullPathConfig)}", color=["Blue", "Bold", None, "Bold", None, "Bold"])

            if permission:
                self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('ERROR.permission_file'), color=["Orange", "Bold", None])

            if err[0]:
                self.console.printLastLine("@ : ", str(err[1]), color=["Red", None])
                self.log.error("❌: " + str(err[1]))

    def unsorted(self, dontSortFileRule: list, source):
        for pathFile in pathlib.Path(source).glob('*.*'):

            nameFile = pathFile.name
            self.log.debug(self.checkedFile)

            if str(nameFile) not in dontSortFileRule and str(nameFile) not in NOT_SORT_LIST and str(nameFile) not in self.checkedFile and str(nameFile) != self.nameAppExe:

                try:
                    shutil.move(pathFile.as_posix(), f"{self.pathDirExe}/{NAME_FOLDER_UNSORTED}/{str(nameFile)}")
                    self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('TERM.move'), f" {NAME_FOLDER_UNSORTED}", color=["Purple", "Bold", None, "Bold"])

                # For permission related errors
                except PermissionError:
                    self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('ERROR.permission_file'), color=["Orange", "Bold", None])

                # For File Exists errors
                except FileExistsError:
                    new = self.duplicate(str(nameFile), f"{self.pathDirExe}/{NAME_FOLDER_UNSORTED}")
                    shutil.move(src = pathFile.as_posix(), dst = f"{self.pathDirExe}/{NAME_FOLDER_UNSORTED}/{new}")
                    self.console.printLastLine("@ : ", f"{str(nameFile)} ", self.langage.t('TERM.rename'), f" {str(new)} ", self.langage.t('TERM.move'), f" {NAME_FOLDER_UNSORTED}", color=["Purple2", "Bold", None, "Bold", None, "Bold"])

                # For other errors
                except OSError as error:
                    self.console.printLastLine("@ : ", str(error), color=["Red", None])
                    self.log.error("❌: " + str(error))

    def __dontSortFiles(self) -> list:
        list_temp = []
        for f in self.conf.CONFIG["doNotSort"]:
            for file in pathlib.Path('./').glob(f):
                list_temp.append(str(file))
        return list_temp

    def duplicate(self, file: str, path: str) -> str:

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

        return newName+fileExt
