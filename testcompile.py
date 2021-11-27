import compileall
import pathlib, os

compileall.compile_dir(dir="func", legacy=True, force=True)
path = "./func/comp"

if not os.path.exists(path):
                os.mkdir(path)
for file in pathlib.Path('./func').glob("*.pyc"):
    os.rename(str(file), path+"/"+file.name)