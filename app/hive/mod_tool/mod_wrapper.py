from __future__ import annotations
from typing import TYPE_CHECKING, Union
from .dig_dug import DigDug
from .py_base import PyBase64

if TYPE_CHECKING:
    from ..worm_construtor import WormConstructor

class ModWrapper:
    def __init__(self, worm_constructor: WormConstructor):
        self.WC = worm_constructor
        self.name = self.WC.name
        self.msg = self.WC.msg
        self.modules = {}
        self.modules["shadow"] = {
            "DigDug" : DigDug(),
            "PyBase64" : PyBase64(self)
        }

    
    def getModule(self, module_type: str, module_name: str) -> Union[object, None]:
        mtype = self.modules.get(module_type)
        if not mtype:
            self.msg("error", f"[!!] ERROR: Module type: {module_type} does not exists in Library. [!!]", sender=self.name)
            return None
        mod = mtype.get(module_name)
        if not mod:
            self.msg("error", f"[!!] ERROR: Module: {module_name} does not exists in {module_type} section. [!!]", sender=self.name)
            return None
        return mod
