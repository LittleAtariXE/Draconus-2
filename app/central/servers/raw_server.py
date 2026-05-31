
from .tcp_server import TcpServer
from ..protocols.basic_tcp import ProtocolBasicTcp
from threading import Lock
from typing import Union
from time import sleep

class RawTcpBuffer:
    def __init__(self, server: object, client_handler: object, encode: str):
        self.server = server
        self.handler = client_handler
        self.timeout = self.server.BUFFER_TIMEOUT
        self.encode_format = encode
        self.lock = Lock()
        self.BUFF = b""
        self.decode_format_list = [self.encode_format, "cp852", "cp1250"]
    
    def buffAdd(self, data: bytes) -> None:
        with self.lock:
            self.BUFF += data
    
    def buffEmpty(self) -> None:
        with self.lock:
            data = self.BUFF
            self.BUFF = b""
        try:
            data = data.decode(self.encode_format, errors="replace")
        except Exception as e:
            data = f"[!!] ERROR decode data from client: {e} [!!]"
        self.server.central.process_msg(data, self.handler)

    
    def buffStart(self) -> None:
        while self.handler.FLAG_connection:
            sleep(self.timeout)
            if self.BUFF == b"":
                continue
            self.buffEmpty()



class RawTcpServer(TcpServer):
    def __init__(self, central: object, name: str, port: int, ip_addr: str = None, is_daemon: bool = True, config: dict = {}):
        super().__init__(central, name, port, ip_addr, is_daemon)
        self.server_type = "Raw"
        if config.get("TCP_SOCKET_FORMAT"):
            self.ENCODE_FORMAT = config.get("TCP_SOCKET_FORMAT")
        else:
            self.ENCODE_FORMAT = self.CONF.tcp_socket_format
        self.protocol = ProtocolBasicTcp(self.FLAG_server_working, self.CONF, self)

        self.BUFFER_TIMEOUT = self.CONF.TCP_RAW_BUFFER_TIMEOUT
        
    

    def recive_data(self, handler: object) -> None:
        buff = RawTcpBuffer(self, handler, self.ENCODE_FORMAT)
        self.central.Tasker.addThread(
            name = f"RawTcpBuff-{handler.ID}",
            func_name = buff.buffStart,
            info = f"Received message buffer for client no.: {handler.ID}",
            daemon = True,
            start_now = True,
            th_type = "Handle"
        )
        while handler.FLAG_connection:
            msg = self.protocol._recive_data(handler)
            if not msg:
                break
            buff.buffAdd(msg)
        handler._close()
    

    def send_data(self, handler: object, data: str) -> None:
        self.protocol.send_data(handler.conn, data)

