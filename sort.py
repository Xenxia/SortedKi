import ntpath
import os
import pathlib
import shutil
from Pylogger import Logger
from Pylang import Lang

from func.conf import ConfigTree

#Page
from page.main import main

NOT_SORT_LIST = ["config.yml", "desktop.ini"]

class Sorting:

    log: Logger
    conf: ConfigTree
    checkedFile: list

    def __init__(self, log: Logger, lang: Lang, conf: ConfigTree, pathDirExe: str, nameAppExe:str, mSort: main) -> None:
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

        self.log.debug("Check Dir", "Sorting-start")

        for name_profile in self.conf.CONFIG['config_sort']:

            disable = self.conf.CONFIG['config_sort'][name_profile]['disable']

            for rule in self.conf.CONFIG['config_sort'][name_profile]['rule']:
                fullPathConfig: str = self.conf.CONFIG['config_sort'][name_profile]['fullPath']
                pathStatic: bool = self.conf.CONFIG['config_sort'][name_profile]['pathStatic']

                if pathStatic:

                    if not os.path.exists(f"{fullPathConfig}"):
                        self.log.debug("Create static Dir : " + f"{self.parentPath}/{fullPathConfig}", "Sorting-start")
                        os.makedirs(f"{fullPathConfig}", exist_ok=True)
                else:

                    if not os.path.exists(f"{self.parentPath}/{fullPathConfig}"):
                        self.log.debug("Create Dir : " + f"{self.parentPath}/{fullPathConfig}", "Sorting-start")
                        os.makedirs(f"{self.parentPath}/{fullPathConfig}", exist_ok=True)

                if rule == "":
                    break

                self.sort(rule, dontSortFileRule, fullPathConfig, self.parentPath, pathStatic, disable)

        if self.conf.CONFIG['unsorted'] == True :
            if not os.path.exists(f"{self.pathDirExe}/#Unsorted"):
                self.log.debug("Create Unsorted Dir", "Sorting-start")
                os.mkdir(f"{self.pathDirExe}/#Unsorted")

            self.unsorted(dontSortFileRule)


    def sort(self, rule: str, dontSortFileRule: list, fullPathConfig: str, parentPath: str, staticPath: bool, disableRule: bool):

        self.log.debug(f"Start sort - rule {rule}", "sort")

        for file in pathlib.Path(self.searchPath).glob(rule):

            file_name = ntpath.basename(file)

            pPath = f"{self.pathDirExe}/{fullPathConfig}"
            futurSortedPathFile = f"{pPath}/{file_name}"

            if staticPath:
                pPath = f"{fullPathConfig}"
                futurSortedPathFile = f"{fullPathConfig}/{file_name}"

            duplica = False
            sort = False
            permission = False
            new = "new"
            err = [False, "none"]

            if str(file_name) not in dontSortFileRule and str(file_name) not in NOT_SORT_LIST and str(file_name) != self.nameAppExe:

                self.log.debug("file_name - "+file_name, "sort")

                self.checkedFile.append(str(file_name))

                if disableRule:
                    continue

                if not os.path.exists(futurSortedPathFile):

                    try:
                        if os.path.isfile(str(file_name)):

                            with open(file_name, "a", encoding="utf8") as file:
                                file.close()

                            shutil.move(str(file_name), futurSortedPathFile)
                            self.log.debug("OK", "sort")
                            sort = True
                        else:
                            self.log.debug(f"Not file {str(file_name)}", "sort")
                            break

                    # For permission related errors
                    except PermissionError:
                        self.log.error("Permission error", "sort")
                        permission = True

                    # For other errors
                    except OSError as error:
                        self.log.error(f"OS error - {error}", "sort")
                        err = [True, error]

                else:
                    try:
                        if os.path.isfile(str(file_name)):
                            self.log.debug(f"Duplicate {file_name}", "sort")
                            new = self.duplicate(str(file_name), f"{pPath}")

                            with open(file_name, "a", encoding="utf8") as file:
                                file.close()
                            
                            shutil.move(src = file_name, dst = f"{pPath}/{new}")
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
                self.console.printLastLine("@ : ", self.langage.t('OK.sorted').format(file=str(file_name), path=fullPathConfig), color=["Green", None])

            if sort and duplica:
                self.console.printLastLine("@ : ", self.langage.t('OK.sorted_double').format(file=str(file_name), new_name=new, path=fullPathConfig), color=["Blue", None])

            if permission:
                self.console.printLastLine("@ : ", self.langage.t('ERROR.permission_file').format(file=str(file_name)), color=["Orange", None])

            if err[0]:
                self.console.printLastLine("@ : ", str(err[1]), color=["Red", None])
                self.log.error("❌: " + str(err[1]))

    def unsorted(self, dontSortFileRule: list):
        for file_path in pathlib.Path(self.pathDirExe).glob('*.*'):

            file_name = ntpath.basename(file_path)

            self.log.debug(self.checkedFile, "UNSORTED")

            if str(file_name) not in dontSortFileRule and str(file_name) not in NOT_SORT_LIST and str(file_name) not in self.checkedFile and str(file_name) != self.nameAppExe:

                try:
                    os.rename(str(file_name), f"{self.pathDirExe}/#Unsorted/{str(file_name)}")
                    self.console.printLastLine("@ : ", self.langage.t('OK.unsorted').format(file=str(file_name)), color=["Purple", None])

                # For permission related errors
                except PermissionError:
                    self.console.printLastLine("@ : ", self.langage.t('ERROR.permission_file').format(file=str(file_name)), color=["Orange", None])

                # For File Exists errors
                except FileExistsError:
                    new = self.duplicate(str(file_name), f"{self.pathDirExe}/#Unsorted")
                    shutil.move(src = str(file_name), dst = f"{self.pathDirExe}/#Unsorted/{new}")
                    self.console.printLastLine("@ : ", self.langage.t('OK.sorted_double_unsorted').format(file=str(file_name), new_name=new), color=["Purple2", None])

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

        # os.rename(file, pathFile)
        

        # while True:
            # if numWhile != 0:
            #     new_name = new_name.replace(new_name[-2:], "_"+str(numWhile))
            # else:
            #     if fileName[-2]!="_":
            #         new_name = fileName+'_'+str(numWhile)
            #     else:
            #         new_name = fileName.replace(fileName[-2:], "_"+str(numWhile+1))

            # new_path = path+'/'+new_name+fileExt
            # if not os.path.exists(new_path):
            #     os.rename(fileName+fileExt, new_path)
            #     break
            # numWhile += 1

        return newName+fileExt
