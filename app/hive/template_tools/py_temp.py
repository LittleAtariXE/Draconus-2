import base64
from typing import Union


class PyTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

    def makeModulesDict(self, modules_list: list) -> str:
        code = "{"
        for mod in modules_list:
            code += f"'{mod}' : {mod},"
        code += " }"
        return code
    
    def buildSortString(self, list_of_list: list, add_char: str = "") -> str:
        database = set()
        for li in list_of_list:
            for l in li:
                if l.startswith(add_char):
                    database.add(l)
                else:
                    database.add(f"{add_char}{l}")
        
        data = " ".join(list(database))
        return data
    
    def encodeHex(self, data: Union[str, bytes], encode: str = "utf-8") -> str:
        if isinstance(data, str):
            data = data.encode(encode)
        return str(data.hex())
    
    def buildLoader(self, script: str, loader: str, replace_char: str = "$") -> str:
        exe_script = loader.replace(replace_char, script)
        return exe_script
    
    def buildListStr(self, text: str, separator: str, prefix: str = None) -> list:
        raw = text.split(separator)
        for i, r in enumerate(raw):
            raw[i] = r.strip()
        if prefix:
            for i, r in enumerate(raw):
                raw[i] = f"{prefix}{raw[i]}"
        return raw
    
    def encodeBase64(self, text: Union[str, bytes], count: int = 1, encode: str = "utf-8") -> str:
        if isinstance(text, str):
            text = text.encode("utf-8")
        etext = text
        for _ in range(count):
            etext = base64.b64encode(etext)
        return etext
    
    def decodeBase64(self, text: Union[str, bytes], count: int = 1, encode: str = "ascii") -> str:
        if isinstance(text, str):
            text = text.encode(encode)
        etext = text
        for _ in range(count):
            etext = base64.b64decode(etext)
        return etext
    
    def decodeBase64Basic(self, text: str) -> bytes:
        return base64.b64decode(text.encode("ascii"))
    
    def getBoolValue(self, text: str) -> str:
        if text == "True" or text == "true" or text == "TRUE":
            return "True"
        else:
            return "False"

        
