
import sys
from .msg_sorter import MessageSorter
from .draco_shell import DraconusShell
from .shell_help import SHELL_HELP_MESSAGES

class MainShell:
    def __init__(self, commander_object: object):
        self.C2 = commander_object
        self.msg_sorter = MessageSorter(self.C2.CONF)
        self.help = SHELL_HELP_MESSAGES(self.msg_sorter)
    
    def Start(self) -> bool:
        if not self.C2.build():
            sys.exit()
        self.draco_shell = DraconusShell(self, self.C2)
        self.draco_shell.Start()
        