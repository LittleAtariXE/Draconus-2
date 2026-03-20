from __future__ import annotations
from typing import Union, TYPE_CHECKING

from .pre_shadow import PreShadowTable

if TYPE_CHECKING:
    from ..coder import Coder


class PreRenderTools:
    def __init__(self, coder: Coder):
        self.coder = coder
        self.msg = self.coder.msg
        self.TOOL_PreShadowTable = PreShadowTable(self)

    def getTool(self, tool_name: str, *args) -> any:
        match tool_name:
            case "duckTable":
                return self.TOOL_PreShadowTable.buildDuckTable(*args)
            case _:
                return ""
    
    def emptyTool(self, *args, **kwargs) -> str:
        return ""