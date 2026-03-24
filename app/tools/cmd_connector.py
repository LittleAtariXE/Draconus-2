import os
import socket
import json

from typing import Union
from .builder import Builder


class CommanderConn:
    def __init__(self, commander: object, builder_object: Builder):
        self.c2 = commander
        self.CONF = builder_object
        self.cmd_socket = None
        
        self.msg_error = self.c2.messages.msgError
        self.msg_basic = self.c2.messages.msgBasic
        self.CMD_SOCKET_FPATH = self.CONF.FD_SOCKET_DRACO_CONTROLER
        self.CMD_SOCKET_TIMEOUT = self.CONF.unix_sock_to_recive
        self.SOCKET_ENCODE = self.CONF.unix_socket_format
        self.CMD_SOCKET_RAW_LEN = self.CONF.unix_socket_raw_len
    

    def cmd_connect(self) -> bool:
        try:
            self.cmd_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.cmd_socket.connect(self.CMD_SOCKET_FPATH)
            return True
        except Exception as e:
            self.msg_error(f"[!!] ERROR Connection to Draconus Controller: {e} [!!]")
            return False


    def build(self) -> bool:
        if not self.cmd_connect():
            return False
        
        return True
    
    def cmd_send_data(self, data: dict) -> bool:
        try:
            jdata = json.dumps(data)
        except json.JSONDecodeError as e:
            self.msg_error(f"[!!] ERROR Encode json command: {e} [!!]")
            return False
        
        try:
            self.cmd_socket.sendall(jdata.encode(self.SOCKET_ENCODE))
        except Exception as e:
            self.msg_error(f"[!!] ERROR send command to Draconus: {e} [!!]")
            return False
        
        return True
    
    def recive_data(self) -> Union[dict, None]:
        self.cmd_socket.settimeout(self.CMD_SOCKET_TIMEOUT)
        msg = b""
        while True:
            try:
                recv = self.cmd_socket.recv(self.CMD_SOCKET_RAW_LEN)
            except TimeoutError:
                self.msg_error("[!!] ERROR: Control Socket Timeout. No response. [!!]")
                break
            except Exception as e:
                self.msg_error(f"[!!] ERROR: Recive response from Control Socket: {e} [!!]")
                break
            if recv:
                if len(recv) < self.CMD_SOCKET_RAW_LEN:
                    msg += recv
                    break
                else:
                    msg += recv
            else:
                break
        
        if msg == b"":
            return None
        try:
            jmsg = json.loads(msg.decode(self.SOCKET_ENCODE))
        except Exception as e:
            self.msg_error(f"[!!] ERROR: Decode JSON response from Control Socket: {e} [!!]")
            return None
        return jmsg
        

        
    

    def cmdSendRaw(self, data: dict) -> None:
        self.cmd_send_data(data)
    

    def cmdReciveData(self) -> Union[dict, None]:
        return self.recive_data()
    
    

    

