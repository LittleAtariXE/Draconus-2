from .raw_lib_item import RawLibItem
from typing import Union

class RawConfigItem(RawLibItem):
    def __init__(self, raw_info_item: object):
        # Module cannot be added to a worm. It has a different purpose.
        self.FLAG_no_worm = True

        # extra library for compiler
        self.PIP_LIB = []



    def _load_data(self, load_type: str, target: Union[str, None]) -> any:
        if not target:
            target = self.raw_code
        match load_type:
            case "list":
                return 
            case _:
                return target
    
    def _load_list(self, target: str) -> list:
        raw = target.split("\n")
        out = []
        for r in raw:
            out.append(r.strip())
        return raw