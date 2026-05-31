import struct
from typing import Union

class RobboMessages:
    def __init__(self, headers: struct, header_sheme: str):
        self._header = headers
        self.header_sheme = header_sheme
        self.raw_data = None
        self.data = None
        self.unpack_headers(headers)
    
    def unpack_headers(self, headers: struct) -> None:
        self.magic, self.types, self.encFlag, self.flags, self.msg_size = struct.unpack(self.header_sheme, headers)
        ##### HEADERS
        # Not used yet
        # uint32_t magic;

        # Message type:
        # 0 - text message
        # 1 - command message
        # 2 - file msg
        # 9 - Empty msg
        # uint8_t types; 

        # Encoded messages
        # 0 - True
        # 1 - False
        # uint8_t encFlag;

        # Other flags
        # uint16_t flags;

        # payload length
        # uint32_t msg_size;
    

class RobboMessagesBuilder:
    def __init__(self, magic: int = 0, types: int = 0, encFlag: int = 0, flags: int = 0):
        self.magic = magic
        self.types = types
        self.encFlag = encFlag
        self.flags = flags
        self.ROBBO_HEADER = "!IBBHI"
        self.ROBBO_HEADER_SIZE = struct.calcsize(self.ROBBO_HEADER)
    
    def build_header(self, data: Union[str, bytes]) -> bytes:
        data_size = len(data)
        head = struct.pack(self.ROBBO_HEADER, self.magic, self.types, self.encFlag, self.flags, data_size)
        return head
    
    def build_send_data(self, data: bytes) -> bytes:
        head = self.build_header(data)
        return head + data

class ProtocolRobboFiveTcp:
    def __init__(self, working_FLAG: object, builder_object: object, server: object):
        self.FLAG_working = working_FLAG
        self.CONF = builder_object
        self.master = server
        self.msg = self.master.msg

        self.TCP_SOCKET_RAW_LEN = self.CONF.tcp_socket_raw_len
        self.TCP_SOCKET_FORMAT = self.master.ENCODE_FORMAT

        self.ROBBO_HEADER = "!IBBHI"
        self.ROBBO_HEADER_SIZE = struct.calcsize(self.ROBBO_HEADER)

    def introduce_decode(self, recv_msg: bytes) -> Union[dict, None]:
        try:
            recv_msg = recv_msg.decode(self.TCP_SOCKET_FORMAT)
        except Exception as e:
            self.msg("error", f"ERROR decode 'introduce client': {e}", sender=self.master.draco_name)
            return None
        key = [recv_msg[n] for n in range(0, len(recv_msg)-1, 5)]
        self.msg("dev", f"Recive encode KEY: {key}", sender=self.master.draco_name)
        return {"ENCODE_KEY" : key}
    
    def decode_data(self, recv_msg: bytes, handler: object) -> str:
        key = "".join(handler.encode_key)
        try:
            key = key.encode(self.TCP_SOCKET_FORMAT)
        except Exception as e:
            self.msg("error", f"[!!] ERROR conversion 'encode key' : {e} [!!]", sender=self.master.draco_name)
            return ""
        msg = bytearray()
        ki = 0
        for b in recv_msg:
            if ki == len(key):
                ki = 0
            msg.append(b ^ key[ki])
            ki += 1
        return msg
    
    def encode_data(self, data: Union[str, bytes], handler: object) -> bytes:
        key = "".join(handler.encode_key)
        
        try:
            key = key.encode(self.TCP_SOCKET_FORMAT)
            if isinstance(data, str):
                data = data.encode(self.TCP_SOCKET_FORMAT)
        except Exception as e:
            self.msg("error", f"[!!] ERROR: Encode send message: {e} [!!]", sender=handler.name)
            return bytearray()
        msg = bytearray()
        ki = 0
        for b in data:
            if ki == len(key):
                ki = 0
            msg.append(b ^ key[ki])
            ki += 1
        return msg
    
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

    def recive_data(self, handle: object) -> Union[RobboMessages, None]:
        rmsg = self._recive_headers(handle)
        if not rmsg:
            return None
        raw_msg = self._recive_data_ex(handle, int(rmsg.msg_size))
        if not raw_msg:
            return None
        rmsg.raw_data = raw_msg
        return rmsg

    def _recive_data_ex(self, handle: object, data_size: int) -> Union[bytes, None]:
        msg = b""
        while handle.FLAG_connection:
            try:
                recv = handle.conn.recv(data_size - len(msg))
            except TimeoutError:
                continue
            except:
                return None
            
            if recv:
                msg += recv
                if (len(msg) == data_size):
                    return msg
                else:
                    continue
            else:
                if msg == b"":
                    return None
                return b""    
    
    def _recive_headers(self, handle: object) -> Union[RobboMessages, None]:
        head = self._recive_data_ex(handle, self.ROBBO_HEADER_SIZE)
        if not head:
            return None
        try:
            rmsg = RobboMessages(head, self.ROBBO_HEADER)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Decode 'ROBBO_HEADER': {e} [!!]", sender=self.master.draco_name)
            return None
        return rmsg
    
    def _send_data(self, conn_obj: object, data: bytes) -> None:
        try:
            conn_obj.sendall(data)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Send data to client: {e} [!!]", sender=self.master.draco_name)
    
    def send_text_data(self, handler: object, data: str) -> None:
        robbo = RobboMessagesBuilder()
        sdata = self.encode_data(data, handler)
        sdata = robbo.build_send_data(sdata)
        # self.msg("dev", f"HEAD: {sdata[0:12]}", sender="DEV")
        self._send_data(handler.conn, sdata)
    
    def send_cmd_data(self, handler: object, data: str) -> None:
        robbo = RobboMessagesBuilder(types=1)
        sdata = self.encode_data(data, handler)
        sdata = robbo.build_send_data(sdata)
        self._send_data(handler.conn, sdata)
    
    def send_file_data(self, handler: object, data: bytes) -> None:
        robbo = RobboMessagesBuilder(types=2, encFlag=1)
        sdata = robbo.build_send_data(data)
        self._send_data(handler.conn, sdata)
    

 
