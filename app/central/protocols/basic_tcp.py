
from typing import Union

class ProtocolBasicTcp:
    def __init__(self, working_FLAG: object, builder_object: object, server: object):
        self.FLAG_working = working_FLAG
        self.CONF = builder_object
        self.master = server

        self.TCP_SOCKET_RAW_LEN = self.CONF.tcp_socket_raw_len
        self.TCP_SOCKET_FORMAT = self.CONF.tcp_socket_format
    

    def _recive_data(self, handle: object) -> Union[bytes, None]:
        msg = b""
        while handle.FLAG_connection:
            try:
                recv = handle.conn.recv(self.TCP_SOCKET_RAW_LEN)
            except TimeoutError:
                continue
            except:
                return None
            
            if recv:
                if len(recv) < self.TCP_SOCKET_RAW_LEN:
                    msg += recv
                    break
                else:
                    msg += recv
            else:
                break

        if msg == b"":
            return None
        else:
            return msg
    
    def recive_data(self, handle: object) -> Union[bytes, None]:
        raw = self._recive_data(handle)
        if not raw:
            return None
        try:
            msg = raw.decode(self.TCP_SOCKET_FORMAT)
        except Exception as e:
            msg = f"[!!] ERROR Decode message: {e} [!!]"
        
        return msg
    

    def _send_data(self, conn_object: object, data: str) -> None:
        try:
            conn_object.sendall(data.encode(self.TCP_SOCKET_FORMAT))
        except:
            pass
    
    def send_data(self, conn_object: object, data: str) -> None:
        self._send_data(conn_object, data)
    
    