import base64
from typing import Union

class CTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    
    def buildTableChar(self, data: str, separator: str, add_null: bool = False) -> str:
        raw = data.split(separator)
        out = ''
        for r in raw:
            out += f'"{r}", '
        if add_null:
            out += "NULL"
        else:
            out = out.rstrip(", ")
        return out
    
    
    def binaryToHex(self, data: bytes, decode_base: bool = True) -> str:
        if decode_base:
            data = base64.b64decode(data.encode("ascii"))
        hex_list = [hex(b) for b in data]
        return ", ".join(hex_list)