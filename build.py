import argparse
import PyInstaller.__main__

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

parser_prod = subparsers.add_parser('prod', help='Build app production',
                                    formatter_class=argparse.RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--version', action='version', version="V1")

args = parser.parse_args()

if args.Command_Name == "dev":
    PyInstaller.__main__.run([
        'tree.py',
        '--onefile',
        '--clean',
        '--add-data=func;func',
        '--add-data=image;image',
        '--add-data=lang;lang',
        '--hidden-import=locale',
        '--hidden-import=ruamel.yaml',
        '--hidden-import=typing',
        '--hidden-import=ctypes',
        '--hidden-import=collections',
        '--hidden-import=sys',
        '--icon=image/tree.ico'
    ])

if args.Command_Name == "prod":
    PyInstaller.__main__.run([
        'tree.py',
        '--onefile',
        '--clean',
        '--windowed',
        '--add-data=func;func',
        '--add-data=image;image',
        '--add-data=lang;lang',
        '--hidden-import=locale',
        '--hidden-import=ruamel.yaml',
        '--hidden-import=typing',
        '--hidden-import=ctypes',
        '--hidden-import=collections',
        '--hidden-import=sys',
        '--icon=image/tree.ico'
    ])