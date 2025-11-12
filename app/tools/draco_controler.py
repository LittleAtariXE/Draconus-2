import os
import socket
import json

from typing import Union

class DracoController:
    def __init__(self, draconus: object):
        self.draconus = draconus
        self.CONF = self.draconus.CONF
        self.Tasker = self.draconus.Tasker
        self.msg = self.draconus.msg

        self.ctrl_server = None
        self.ctrl_conn = None
        self.ctrl_addr = None

        self.UNIX_RAW_LEN = self.CONF.unix_socket_raw_len
        self.ENCODE_FORMAT = self.CONF.unix_socket_format
        self.SOCKET_FPATH = self.CONF.FD_SOCKET_DRACO_CONTROLER
        self.SOCKET_TIMEOUT = self.CONF.unix_sock_to_recive

        self.FLAG_ERROR = False
    
    @property
    def FLAG_working(self) -> bool:
        return self.draconus.FLAG_working
    

    def build(self) -> bool:
        if os.path.exists(self.SOCKET_FPATH):
            try:
                os.unlink(self.SOCKET_FPATH)
            except:
                pass
        try:
            self.ctrl_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.ctrl_server.bind(self.SOCKET_FPATH)
            self.ctrl_server.listen(1)
            self.msg("msg", "Socket Controller build successfull.")
            return True
        except Exception as e:
            self.msg("error", f"[!!] ERROR Build control socket: {e} [!!]")
            return False
    
    def accept_conn(self) -> None:
        self.ctrl_server.settimeout(self.SOCKET_TIMEOUT)
        while self.FLAG_working:
            try:
                self.ctrl_conn, self.ctrl_addr = self.ctrl_server.accept()
            except TimeoutError:
                continue
            self.msg("msg", "Connected to Draconus")
            self.recive_cmd()
    
    def recive_data(self) -> Union[dict, None]:
        msg = b""
        while self.FLAG_working:
            try:
                recv = self.ctrl_conn.recv(self.UNIX_RAW_LEN)
            except TimeoutError:
                continue
            except:
                return None
            
            if recv:
                if len(recv) < self.UNIX_RAW_LEN:
                    msg += recv
                    break
                else:
                    msg += recv
            else:
                break
        
        if msg == b"":
            return None
        try:
            jdata = json.loads(msg.decode(self.ENCODE_FORMAT))
        except json.JSONDecodeError as e:
            self.msg("error", f"[!!] ERROR: decode JSON command: {e} [!!]")
            return {}
        
        return jdata
    
    def recive_cmd(self) -> None:
        while self.FLAG_working:
            cmd = self.recive_data()
            if not cmd:
                break
            self.process_cmd(cmd)
        
        if self.FLAG_working:
            self.FLAG_ERROR = 1
            # self.msg("error", "[!!] ERROR: DracoController lost connection. [!!]")
    
    def send_data(self, data: dict) -> None:
        try:
            data = json.dumps(data)
        except json.JSONDecodeError as e:
            self.msg("error", f"[!!] ERROR Draconus Controler encode JSON: {e} [!!]")
            return
        try:
            self.ctrl_conn.sendall(data.encode(self.ENCODE_FORMAT))
        except Exception as e:
            self.msg("error", f"[!!] ERROR Draconus Controler send data: {e} [!!]")
            

    def Start(self) -> None:
        self.Tasker.addThread("DracoController", self.accept_conn, info="Receives and executes commands from Commander.", daemon=True)
        
    def process_cmd(self, cmd: dict) -> None:
        main = cmd.get("cmd_type")
        if not main:
            self.msg("error", "[!!] ERROR: No main command. [!!]")
            return
        match main:
            case "sys":
                self.draconus.execute_sys_cmd(cmd)
            case _:
                self.msg("error", f"[!!] ERROR: Unknown type command: '{main}'. [!!]")
        
    
