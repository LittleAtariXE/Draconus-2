from __future__ import annotations
import string
import os
from typing import Union, TYPE_CHECKING
from random import choice

from .tcp_server import TcpServer
from ..protocols.basic_tcp import ProtocolBasicTcp

if TYPE_CHECKING:
    from ..central import Central, ClientHandler


class RawDown(TcpServer):
    def __init__(self, central: Central, name: str, port: int, ip_addr: str = None, is_daemon: bool = True, config: dict = {}):
        super().__init__(central, name, port, ip_addr, is_daemon)
        self.server_type = "RawDown"
        self.FIRST_JOB = "recive"
        if config.get("TCP_SOCKET_FORMAT"):
            self.ENCODE_FORMAT = config.get("TCP_SOCKET_FORMAT")
        else:
            self.ENCODE_FORMAT = self.CONF.tcp_socket_format
        self.protocol = ProtocolBasicTcp(self.FLAG_server_working, self.CONF, self)
        self.DIR_LOOT_MAIN = self.CONF.DIR_LOOT
        self.DIR_LOOT = os.path.join(self.DIR_LOOT_MAIN, self.server_name)
        self.FILE_NAME_LENGTH = 16
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
    

    def genFileName(self, char_len: int = 10) -> str:
        name = ""
        while len(name) < char_len:
            name += choice(self.chars_data)
        return name
    
    def saveLoot(self, file_data: bytes) -> None:
        file_name = self.genFileName(self.FILE_NAME_LENGTH)
        try:
            with open(os.path.join(self.DIR_LOOT, file_name), "wb") as file:
                file.write(file_data)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Save loot file: {e} [!!]", sender=self.draco_name)
            return
        self.msg("no_imp", f"Save file: {file_name} in loot dir: {self.DIR_LOOT} successfull.", sender=self.draco_name)
    
    def recive_data(self, handler: ClientHandler) -> None:
        while handler.FLAG_connection:
            file_data = self.protocol._recive_data(handler)
            if not file_data:
                break
            self.saveLoot(file_data)

        handler._close()
    
    def send_data(self, handler: ClientHandler, data: any) -> None:
        self.protocol.send_data(handler.conn, data)

