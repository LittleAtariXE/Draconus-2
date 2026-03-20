import string
from random import choice


class PreShadowTable:
    def __init__(self, pre_master: object):
        self.master = pre_master
        self.LAYER_CHAR_DEFAULT = string.ascii_letters + string.digits + "_" + "." + " " + ":" + '"' + "-"
    
    def buildDuckTable(self, *args) -> dict:
        # args: data, base_char
        if len(args) < 2:
            data = args[0]
            base_chars = self.LAYER_CHAR_DEFAULT
        else:
            data = args[0]
            base_chars = args[1]
        if not base_chars:
            base_chars = self.LAYER_CHAR_DEFAULT
        chars = {}
        for char in base_chars:
            chars[char] = []
        base = list(data)
        for index, char in enumerate(base):
            if not char in chars.keys():
                continue
            chars[char].append(index)
        return chars
    
    def digitsEncode(text: str, obf_chars: dict, add_zero: bool = True) -> str:
        code = []
        for char in text:
            if not char in obf_chars.keys():
                continue
            code.append(str(choice(obf_chars[char])))
        if add_zero:
            code.append("0")
        return ", ".join(code)


