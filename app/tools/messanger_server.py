import socket
import json
import os

from tabulate import tabulate
from datetime import datetime
from threading import Lock, Thread
from typing import Union
from time import sleep

from .builder import Builder


class MessangerServer:
    def __init__(self, builder_object: Builder, name: str):
        self.CONF = builder_object
        self.name = name
        self.lock = self.CONF.LOCK_TH_DRACONUS_LOGS
        self.socket_lock = Lock()
        self.buffer_lock = Lock()
        self.server = None
        self.sock_conn = None
        self.sock_addr = None
        self.messanger_th = None
        
        self.ENCODE_FORMAT = self.CONF.unix_socket_format
        self.DEFAULT_TABLE_STYLE = self.CONF.MSG_DEFAULT_TABLE_STYLE
        self.FIRST_TABLE_SPACE = self.CONF.MSG_FIRST_TABLE_SPACE
        self.FPATH_LOG_FILE = self.CONF.PATH_DRACONUS_LOGS
        self.FPATH_SOCKET = self.CONF.FD_SOCKET_DRACO_MSG
        self.CONSOLE_SCR = self.CONF.console_screen
        self.SEND_MSG_PAUSE = self.CONF.MSG_PAUSE_UNIX_SEND
        self.UNIX_SOCKET_SEPRATOR = self.CONF.MSG_UNIX_SEPARATOR
        self.NOT_SHOW = set()
        self.BUFFER = []

    @property
    def date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ########## SERVER #############################

    def build_socket(self) -> bool:
        if os.path.exists(self.FPATH_SOCKET):
            try:
                os.unlink(self.FPATH_SOCKET)
            except Exception as e:
                print(f"[!!] ERROR unlink socket file descriptor: {e} [!!]")
                return False
        
        try:
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.server.bind(self.FPATH_SOCKET)
            self.server.listen()
        except Exception as e:
            print(f"[!!] ERROR building socket: {e} [!!]")
            return False
        
        return True
    
    def listening(self) -> None:
        while True:
            self.sock_conn, self.sock_addr = self.server.accept()
            self.empty_buffer()
    

    def start_server(self) -> None:
        if not self.build_socket():
            return
        self.messanger_th = Thread(target=self.listening, daemon=True)
        self.messanger_th.start()
    
    def add_to_buffer(self, msg_dict: dict) -> None:
        with self.buffer_lock:
            self.BUFFER.append(msg_dict)
    
    def send_msg(self, msg_dict: dict) -> None:
        sleep(self.SEND_MSG_PAUSE)
        if not self.sock_conn:
            self.BUFFER.append(msg_dict)
            return
        try:
            jmsg = json.dumps(msg_dict)
            jmsg += self.UNIX_SOCKET_SEPRATOR
        except Exception as e:
            self.add_log_txt(f"[!!] ERROR encode json: {e} [!!]", sender=self.name)
            jmsg = self._build_messages("error", f"[!!] ERROR encode json: {e} [!!]", sender=self.name)
            jmsg = json.dumps(jmsg)
            jmsg += self.UNIX_SOCKET_SEPRATOR
            self.send_msg(jmsg)
        with self.socket_lock:
            try:
                self.sock_conn.sendall(jmsg.encode(self.ENCODE_FORMAT))
            except Exception as e:
                self.add_to_buffer(msg_dict)
    
    ################################################################################################

    def make_log_file(self) -> None:
        if not os.path.exists(self.FPATH_LOG_FILE):
            with open(self.FPATH_LOG_FILE, "w") as file:
                file.write(f"START LOG FILE: {self.date}\n")
                file.write("-" * 100 + "\n\n")
    

    def add_log_txt(self, msg: str, sender: str, no_separator: bool = False) -> None:
        with self.lock:
            with open(self.FPATH_LOG_FILE, "a+") as file:
                if no_separator:
                    file.write(msg)
                else:
                    file.write("-" * 100 + "\n")
                    file.write(f"[{self.date}][{sender}] {msg}\n")
    
    ########################### MESSAGES #######################################################

    def _build_messages(self, types: str, msg: str, sender: str = None, no_separator: bool = False) -> dict:
        if not sender:
            sender = self.name
        smsg = {
            "types" : types,
            "msg" : msg,
            "sender" : sender,
            "no_separator" : no_separator,
            "date" : self.date
        }

        return smsg


    def _build_table(self, msg: dict, no_separator: bool = False) -> str:
        # data - list
        # headers - list
        # width - list
        # types - str tableFMT
        headers = msg.get("headers", [])
        data = msg.get("data", [])
        # add space to first element
        for d in data:
            d[0] = f"{self.FIRST_TABLE_SPACE}{d[0]}"
        width = msg.get("width")
        if not isinstance(width, list):
            width = list(width)
        types = msg.get("types", self.DEFAULT_TABLE_STYLE)
        table = tabulate(data, headers=headers, tablefmt=types, maxcolwidths=width, disable_numparse=True)
        if no_separator:
            return table
        else:
            return "\n" + table
    
    def _build_title(self, msg: Union[str, list, dict], no_separator: bool = False) -> str:
        if not isinstance(msg, str):
            msg = str(msg)
        ltitle = self.CONSOLE_SCR["slen"] - len(msg)
        ltitle = int((ltitle / 2) - 10)
        ltitle = "*" * ltitle
        msg = f"{ltitle}{msg}{ltitle}"
        if no_separator:
            return msg
        else:
            return "\n" + msg
    
    def empty_buffer(self) -> None:
        if len(self.BUFFER) == 0:
            return
        #self.work("msg", "  Missed Messages  ", mtypes="title")
        with self.buffer_lock:
            for b in self.BUFFER:
                self.send_msg(b)
            self.BUFFER = []
    
    def process_msg(self, msg: Union[str, dict, list], mtypes: str = None, no_separator: bool = False) -> str:
        if mtypes:
            match mtypes:
                case "title":
                    msg = self._build_title(msg, no_separator)
                case "table":
                    msg = self._build_table(msg, no_separator)
        return msg
    
    ####################################################################################################################################
    
    def work(self, types: str, msg: Union[str, list, dict], sender: str = "Draconus", mtypes: str = None, color: str = None, extCONF: dict = {}, no_separator: bool = False) -> None:
        msg = self.process_msg(msg, mtypes, no_separator)
        self.add_log_txt(msg, sender, no_separator)
        msg_dict = self._build_messages(types, msg, sender, no_separator)
        self.send_msg(msg_dict)
    
    def logOnly(self, msg: Union[str, list, dict], sender: str = "Draconus", mtypes: str = None, no_separator: bool = False) -> None:
        msg = self.process_msg(msg, mtypes, no_separator)
        self.add_log_txt(msg, sender, no_separator)

    
    def Start(self) -> None:
        self.make_log_file()
        self.start_server()
    
    def __call__(self, types: str, msg: Union[str, list, dict] = "", sender: str = "Draconus", mtypes: str = None, color: str = None, extCONF: dict = {}, no_separator: bool = False, log_only: bool = False) -> None:
        if log_only:
            self.logOnly(msg, sender, mtypes, no_separator)
        else:
            self.work(types, msg, sender, mtypes, color, extCONF, no_separator)
        


