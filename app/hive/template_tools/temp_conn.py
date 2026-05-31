import string
from random import choice
from typing import Union

class ConnTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    


    def fiveGenKey(self, key_len: int = 5, add_zero: bool = True) -> str:
        layer = string.ascii_letters + string.digits
        skey = ""
        for _ in range(key_len * 5):
            skey += choice(layer)
        key = [f"{hex(ord(x))}" for x in skey]
        if add_zero:
            key.append("0x00")
        return ", ".join(key)


    def fiveSetKey(self, key: str, add_zero: bool = True) -> str:
        layer = string.ascii_letters + string.digits
        skey = []
        key_len = len(key)
        kindex = 0
        for b in range(key_len * 5):
            if b % 5 == 0:
                skey.append(hex(ord(key[kindex])))
                kindex += 1
            else:
                skey.append(hex(ord(choice(layer))))
        return ", ".join(skey)


