from datetime import datetime
import getpass
import logging
from os import terminal_size
from typing import ContextManager

logging.basicConfig()

time = datetime.now()
user = getpass.getuser()

def test():
    print(__name__)

class test2():

    def __init__(self) -> None:
        pass

print(test2.__name__)
