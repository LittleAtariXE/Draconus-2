from __future__ import annotations
import os
from typing import Union, TYPE_CHECKING
from .tcp_server import TcpServer
from ..protocols.basic_tcp_no_encode import ProtocolBasicTcpNoEncode

if TYPE_CHECKING:
    from ..central import Central, ClientHandler


class DeliverTcpServer(TcpServer):
    def __init__(self, central: Central, name: str, port: int, ip_addr: str = None, is_daemon: bool = True, config: dict = {}):
        super().__init__(central, name, port, ip_addr, is_daemon)
        self.server_type = "deliver"
        self.central = central
        self.SERVER_DIR_INPUT = os.path.join(self.DIR_INPUT_PATH, self.draco_name)
        self.FIRST_JOB = "raw_send"
        self.make_send_dir()
    

    def make_send_dir(self) -> bool:
        if not os.path.exists(self.SERVER_DIR_INPUT):
            try:
                os.mkdir(self.SERVER_DIR_INPUT)
                self.msg("msg", f"Making input directory: {self.SERVER_DIR_INPUT}.", sender=self.draco_name)
            except Exception as e:
                self.msg("error", f"[!!] ERROR: Making input directory: {e} [!!]", sender=self.draco_name)
    
    def getFile(self) -> Union[str, None]:
        if not os.path.exists(self.SERVER_DIR_INPUT):
            return None
        for file in os.listdir(self.SERVER_DIR_INPUT):
            return os.path.join(self.SERVER_DIR_INPUT, file)
        return None
    
    def recive_data(self, handler: ClientHandler) -> None:
        # Server does not recive any data
        pass
    
    def send_raw_data(self, handler: ClientHandler) -> None:
        fpath = self.getFile()
        if not fpath:
            self.msg("error", f"[!!] ERROR: Can't send file to client. Directory: {self.SERVER_DIR_INPUT} is empty.", sender=self.draco_name)
            return
        self.msg("msg", f"Start send file: {os.path.basename(fpath)} ....", sender=self.draco_name)
        try:
            with open(fpath, "rb") as file:
                handler.conn.sendfile(file, 0)
            self.msg("msg", f"Send file: {os.path.basename(fpath)} complete.", sender=self.draco_name)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Send file: {e} [!!]", sender=self.draco_name)
        handler._close()

    


