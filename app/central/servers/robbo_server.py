import os
import socket
import string

from threading import Thread, Event, Lock
from time import sleep
from typing import Union
from random import choice

from .tcp_server import TcpServer
from ..protocols.robbo_5_tcp import ProtocolRobboFiveTcp
from ..protocols.robbo_5_tcp import RobboMessages


class RobboTcpServer(TcpServer):
    def __init__(self, central: object, name: str, port: int, ip_addr: str = None, is_daemon: bool = True, config: dict = {}):
        super().__init__(central, name, port, ip_addr, is_daemon)
        self.server_type = "rTCP"
        if config.get("TCP_SOCKET_FORMAT"):
            self.ENCODE_FORMAT = config.get("TCP_SOCKET_FORMAT")
        else:
            self.ENCODE_FORMAT = self.CONF.tcp_socket_format
        self.protocol = ProtocolRobboFiveTcp(self.FLAG_server_working, self.CONF, self)

        ## Length of the "introduce yourself" message
        self.introduce_length = 1024
        ## Time
        self.introduce_timeout = 2

        self.DIR_LOOT_MAIN = self.CONF.DIR_LOOT
        self.DIR_LOOT = os.path.join(self.DIR_LOOT_MAIN, self.server_name)
        self.DIR_INPUT = self.CONF.DIR_INPUT
        self.FILE_NAME_LENGTH = 24
        self.chars_data = string.ascii_letters + string.digits
        self._build()
    
    def _build(self) -> None:
        if not os.path.exists(self.DIR_LOOT_MAIN):
            try:
                os.mkdir(self.DIR_LOOT_MAIN)
            except Exception as e:
                self.msg("error", f"[!!] ERROR: Making Loot directories. Server will not function properly. Error: {e}. [!!]", sender=self.draco_name)
                return
        if not os.path.exists(self.DIR_LOOT):
            try:
                os.mkdir(self.DIR_LOOT)
            except Exception as e:
                self.msg("error", f"[!!] ERROR: Making Server Loot directories. Server will not function properly. Error: {e}. [!!]", sender=self.draco_name)
                return
        self.msg("msg", f"Making loot directory: {self.DIR_LOOT}.", sender=self.draco_name)

    def accept_connections(self, conn: object, addr: object) -> None:
        th = Thread(target=self.introduce_client, args=(conn, addr), daemon=True)
        th.start()


    def introduce_client(self, conn: object, addr: object) -> None:
        self.msg("msg", f"Client: {addr[0]}:{addr[1]} trying connect......", sender=self.draco_name)
        conn.settimeout(self.introduce_timeout)
        try:
            recv = conn.recv(self.introduce_length)
        except TimeoutError:
            self.msg("msg", f"Client: {addr[0]}:{addr[1]} didn't have time to introduce himself.", sender=self.draco_name)
            return
        except Exception as e:
            self.msg("error", f"Client: {addr[0]}:{addr[1]} introduce error: {e}", sender=self.draco_name)
            self.close_stranger(conn)
            return
        if not recv:
            self.close_stranger(conn)
            self.msg("error", f"Client: {addr[0]}:{addr[1]} don't want to introduce myself.", sender=self.draco_name)
        else:
            client_key = self.protocol.introduce_decode(recv)
            if not client_key:
                self.msg("error", f"[!!] ERROR: Can't decode key from: {addr[0]}:{addr[1]} [!!]", sender=self.draco_name)
                self.close_stranger(conn)
                return
            self.central.add_new_connection(conn, addr, self, client_key)


    def close_stranger(self, conn: object) -> None:
        try:
            conn.close()
        except Exception as e:
            self.msg("dev", f"[DEV-ERROR] ERROR: Close stranger client: {e}", sender=self.draco_name)
    
    def recive_data(self, handler: object) -> None:
        while handler.FLAG_connection:
            rmsg = self.protocol.recive_data(handler)
            if not rmsg:
                break
            msg = self.process_headers(handler, rmsg)
            if not msg:
                continue
            self.central.process_msg(msg, handler)
        handler._close()
    
    def genFileName(self, char_len: int = None) -> str:
        if not char_len:
            char_len = self.FILE_NAME_LENGTH
        name = ""
        while len(name) < char_len:
            name += choice(self.chars_data)
        return name
    
    def _process_text_data(self, handler: object, rmsg: RobboMessages) -> None:
        try:
            rmsg.data = rmsg.data.decode(self.ENCODE_FORMAT)
        except Exception as e:
            self.msg("error", f"[!!] ERROR: decode text messages: {e} [!!]", sender=self.draco_name)
    
    def _process_command_data(self, handler: object, rmsg: RobboMessages) -> None:
        rmsg.data = "EXECUTE COMMAND"

    def _process_file_data(self, handler: object, rmsg: RobboMessages) -> None:
        fname = self.genFileName()
        try:
            with open(os.path.join(self.DIR_LOOT, fname), "wb") as file:
                file.write(rmsg.raw_data)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Saving loot from Client <{handler.ID}>. Error: {e}", sender=self.dracon_name)
            rmsg.data = None
            return
        self.msg("msg", f"Download and save new file: {fname} from Client {handler.name}", sender=self.draco_name)
        rmsg.data = None
    
    def process_headers(self, handler: object, rmsg: RobboMessages) -> Union[str, None]:
        if rmsg.encFlag == 0:
            rmsg.data = self.protocol.decode_data(rmsg.raw_data, handler)
        else:
            rmsg.data = rmsg.raw_data
        match rmsg.types:
            case 0:
                self._process_text_data(handler, rmsg)
            case 1:
                self.msg("no_imp", f"Start download file from client: {handler.name} .......", sender=self.draco_name)
                self._process_command_data(handler, rmsg)
            case 2:
                self._process_file_data(handler, rmsg)
            case 9:
                return None
        return rmsg.data
    
    def send_data(self, handler: object, data: str) -> None:
        self.protocol.send_cmd_data(handler, data)
    
    def send_file(self, handler: object, fname: str, **kwargs) -> None:
        self.msg("msg", f"Send file: {fname} to {handler.name} ...", sender=self.draco_name)
        fpath = os.path.join(self.DIR_INPUT, fname)
        try:
            with open(fpath, "rb") as file:
                data = file.read()
        except Exception as e:
            self.msg("error", f"[!!] ERROR Read data from file: {fname}. Error: {e} [!!]", sender=self.draco_name)
            return
        self.protocol.send_file_data(handler, data)
        self.msg("msg", f"Send file to: {handler.name} successfull.", sender=self.draco_name)
        