import json
from .builder import Builder
from typing import Union


class UnixMsgDecode:
    def __init__(self, commander: object, builder_object: Builder):
        self.CONF = builder_object
        self.commander = commander
        self.msgError = self.commander.messages.msgError
        self.msgBasic = self.commander.messages.msgBasic

        self.UNIX_SEPARATOR = self.CONF.MSG_UNIX_SEPARATOR
        self.UNIX_ENCODE_FORMAT = self.CONF.unix_socket_format


    
    def split_msg(self, raw_data: str) -> list:
        data = []
        for rd in raw_data.split(self.UNIX_SEPARATOR):
            if rd == "" or rd == "\n" or rd == " ":
                continue
            data.append(rd)
        return data

    def decode_unix_msg(self, raw: bytes) -> list:
        try:
            rdata = raw.decode(self.UNIX_ENCODE_FORMAT)
        except Exception as e:
            self.msgError(f"[!!] ERROR: decode messages: {e} [!!]")
            return []
        
        raw_msg = []
        rdata = self.split_msg(rdata)
        for rd in rdata:
            try:
                raw_msg.append(json.loads(rd))
            except json.JSONDecodeError as e:
                self.msgError(f"[!!] ERROR message json decode: {e} [!!]")
                
        return raw_msg  
