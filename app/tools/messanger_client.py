import json
import socket

from threading import Thread, Lock
from termcolor import cprint
from typing import Union
from .builder import Builder
from .unix_msg_protocol import UnixMsgDecode

class MessangerClient:
    def __init__(self, builder_object: Builder, commander_object: object, name: str = "Commander"):
        self.name = name
        self.CONF = builder_object
        self.Commander = commander_object
        self.UMD = UnixMsgDecode(self.Commander, self.CONF)
        self.FLAG_ERROR = False

        self.ENCODE_FORMAT = self.CONF.unix_socket_format
        self.SOCKET_RAW_LEN = self.CONF.unix_socket_raw_len
        self.SOCKET_TIMEOUT = self.CONF.unix_sock_to_recive
        self.SOCKET_FPATH = self.CONF.FD_SOCKET_DRACO_MSG

        self.colors = {
            "msg" : self.CONF.msg_color_basic,
            "error" : self.CONF.msg_color_error,
            "no_imp" : self.CONF.msg_color_no_imp,
            "dev" : "blue",
        }


        self.socket = None
        self.TH_msg = None
    
    @property
    def FLAG_working(self) -> bool:
        return self.Commander.FLAG_working
    
    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(self.SOCKET_FPATH)
            self.socket.settimeout(self.SOCKET_TIMEOUT)
            return True
        except Exception as e:
            self._MSG_ERROR(e, self.name)
            return False
        
    def _recive_data(self) -> Union[list, None]:
        msg = b""
        while self.FLAG_working:
            try:
                recv = self.socket.recv(self.SOCKET_RAW_LEN)
            except TimeoutError:
                continue
            except:
                return None
            
            if recv:
                if len(recv) < self.SOCKET_RAW_LEN:
                    msg += recv
                    break
                else:
                    msg += recv
            else:
                return None
        if msg == b"":
            return None
        
        clean_msg = self.UMD.decode_unix_msg(msg)
        return clean_msg

    
    def _recive_msg(self) -> None:
        while self.FLAG_working:
            data = self._recive_data()
            if not data:
                break
            self.show_msg(data)
        if self.FLAG_working:
            self._MSG_ERROR("Lost connection to Draconus", self.name)
            self.FLAG_ERROR = True
        else:
            try:
                self.socket.close()
            except:
                pass
        
    
    def recive_msg(self) -> None:
        self.TH_msg = Thread(target=self._recive_msg, daemon=True)
        self.TH_msg.start()
    
    def show_msg(self, msg_pack: list) -> None:
        for msg in msg_pack:
            self._show_msg(msg)
    
    def _show_msg(self, data: dict) -> None:
        if not isinstance(data, dict):
            return
        if data.get("no_separator"):
            cprint(data["msg"], self.colors[data['types']])
        else:
            cprint(f"\n[{data['sender']}] {data['msg']}", self.colors[data['types']])
    
    def _MSG_ERROR(self, text: str, sender: str) -> None:
        msg = {
            "types" : "error",
            "msg" : f"[!!] ERROR: {text} [!!]",
            "sender" : sender
        }

        self.show_msg(msg)

    def Start(self) -> bool:
        if not self.connect():
            return False
        self.recive_msg()
        return True


