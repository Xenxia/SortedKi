import argparse
import os, pathlib, shutil
import PyInstaller.__main__
import compileall

APP_NAME = "SortedTree"

parser = argparse.ArgumentParser(description="app to build Tree",
                                 allow_abbrev=False,
                                 prog='Build',
                                 usage='%(prog)s'
                                 )

subparsers = parser.add_subparsers(title='Commande',
                                   dest='Command_Name',
                                   )

parser_dev = subparsers.add_parser('dev', help='Build app development',
                                    formatter_class=argparse.RawTextHelpFormatter)

# parser_prod = subparsers.add_parser('prod', help='Build app production',
#                                     formatter_class=argparse.RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--version', action='version', version="V1")

args = parser.parse_args()

compileall.compile_dir(dir="func", legacy=True, force=True)
compileall.compile_dir(dir="page", legacy=True, force=True)

path = ["./func", "./page"]

for p in path:
    p = f"{p}/comp"
    if os.path.exists(p):
        shutil.rmtree(p)

for p in path:
    p = f"{p}/comp"
    os.mkdir(p)

# move file.pyc to ./comp
for p in path:
    for file in pathlib.Path(p).glob("*.pyc"):
        os.rename(str(file), f"{p}/comp/{file.name}")

print("\n=========================================== BUILD DEV ===========================================\n")
PyInstaller.__main__.run([
    f'{APP_NAME.lower()}.py',
    f'--name={APP_NAME}_dev',
    '--onefile',
    # '--clean',
    '--add-data=func/comp;func',
    '--add-data=page/comp;page',
    '--add-data=img;img',
    '--add-data=lang;lang',
    '--hidden-import=locale',
    '--hidden-import=ruamel.yaml',
    '--hidden-import=typing',
    '--hidden-import=ctypes',
    '--hidden-import=sys',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.scrolledtext',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter',
    '--hidden-import=requests',
    '--hidden-import=webbrowser',
    '--hidden-import=Tk-up',
    '--icon=img/tree.ico'
])
print("\n========================================= END BUILD DEV ==========================================\n")

if not args.Command_Name == "dev":
    print("=========================================== BUILD PROD ===========================================\n")
    PyInstaller.__main__.run([
        f'{APP_NAME.lower()}.py',
        f'--name={APP_NAME}',
        '--onefile',
        # '--clean',
        '--windowed',
        '--add-data=func/comp;func',
        '--add-data=page/comp;page',
        '--add-data=img;img',
        '--add-data=lang;lang',
        '--hidden-import=locale',
        '--hidden-import=ruamel.yaml',
        '--hidden-import=typing',
        '--hidden-import=ctypes',
        '--hidden-import=sys',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter',
        '--hidden-import=requests',
        '--hidden-import=webbrowser',
        '--hidden-import=Tk-up',
        '--icon=img/tree.ico'
    ])
    print("\n========================================= END BUILD PROD ==========================================\n")

for p in path:
    p = f"{p}/comp"
    if os.path.exists(p):
        shutil.rmtree(p)
