import argparse
import os, pathlib, shutil
import PyInstaller.__main__
import compileall

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
path = "./func/comp"

if os.path.exists(path):
    shutil.rmtree(path)

os.mkdir(path)

# move file.pyc to ./comp
for file in pathlib.Path('./func').glob("*.pyc"):
    os.rename(str(file), path+"/"+file.name)

print("\n=========================================== BUILD DEV ===========================================\n")
PyInstaller.__main__.run([
    'tree.py',
    '--name=Tree_dev',
    '--onefile',
    # '--clean',
    '--add-data=func/comp;func',
    '--add-data=image;image',
    '--add-data=lang;lang',
    '--hidden-import=locale',
    '--hidden-import=ruamel.yaml',
    '--hidden-import=typing',
    '--hidden-import=ctypes',
    '--hidden-import=sys',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter',
    '--icon=image/tree.ico'
])
print("\n========================================= END BUILD DEV ==========================================\n")

if not args.Command_Name == "dev":
    print("=========================================== BUILD PROD ===========================================\n")
    PyInstaller.__main__.run([
        'tree.py',
        '--name=Tree',
        '--onefile',
        # '--clean',
        '--windowed',
        '--add-data=func/comp;func',
        '--add-data=image;image',
        '--add-data=lang;lang',
        '--hidden-import=locale',
        '--hidden-import=ruamel.yaml',
        '--hidden-import=typing',
        '--hidden-import=ctypes',
        '--hidden-import=sys',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter',
        '--icon=image/tree.ico'
    ])
    print("\n========================================= END BUILD PROD ==========================================\n")

if os.path.exists(path):
    shutil.rmtree(path)