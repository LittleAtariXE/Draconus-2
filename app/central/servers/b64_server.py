import base64
from .tcp_server import TcpServer
from ..protocols.basic_tcp_no_encode import ProtocolBasicTcpNoEncode



class B64TcpServer(TcpServer):
    def __init__(self, central: object, name: str, port: int, ip_addr: str = None, is_daemon: bool = True):
        super().__init__(central, name, port, ip_addr, is_daemon)
        self.server_type = "b64"
        self.protocol = ProtocolBasicTcpNoEncode(self.FLAG_server_working, self.CONF, self)
    

    def recive_data(self, handler: object) -> None:
        while handler.FLAG_connection:
            msg = self.protocol._recive_data(handler)
            if not msg:
                break
            self.process_msg(msg, handler)
        handler._close()
    
    def process_msg(self, msg: bytes, handler: object) -> None:
        #msg = msg.decode(self.CONF.tcp_socket_format)
        try:
            msg = base64.b64decode(msg)
        except Exception as e:
            msg = f"[!!] ERROR Decode message from base64: {e} [!!]"
        try:
            msg = msg.decode(self.CONF.tcp_socket_format)
        except Exception as e:
            msg = f"[!!] ERROR Decode to string: {e} [!!]"


        self.central.process_msg(msg, handler)
    
    def send_data(self, handler: object, data: str) -> None:
        try:
            data = base64.b64encode(data.encode(self.CONF.tcp_socket_format))
        except Exception as e:
            self.msg("error", f"[!!] ERROR Encode data to base64: {e} [!!]", sender=self.server_name)
            return
        self.protocol.send_data(handler.conn, data)