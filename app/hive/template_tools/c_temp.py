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
    
    
