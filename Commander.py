# from app.tools.builder import Builder
# from app.cc.commander import Commander
# from app.shell.main import MainShell

import os   
from app.tools.builder import Builder
from app.commander import Commander
from app.shell.main_shell import MainShell

if __name__ == "__main__":
    os.system("clear")
    CC = Commander(Builder())
    master = MainShell(CC)
    master.Start()
    # shell = MainShell(CC)
    # shell.Run()
