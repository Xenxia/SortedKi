import os

fileName, fileExt = os.path.splitext("test_blue_[1231234567898].test")

numberDuplicate = 1
end = False
index = 0
forcePass = False
newName: str

for s in range(500):

    if fileName[-1] != "]" or forcePass:
        print("pass")
        newName = f"{fileName}_[{numberDuplicate}]"
        numberDuplicate += 1
    else:
        if not end:
            print("end")
            if "_[" in fileName and "]" in fileName:
                for i in range(12+4):
                    i_N = (i*-1)
                    if "_[" == fileName[i_N:(i_N+2)]:
                        print("break")
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

    pathFile = f"{newName}{fileExt}"
    
print(index, " : ", newName, " : ", " : ", fileExt)
