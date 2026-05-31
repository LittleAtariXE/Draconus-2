
from typing import Union

class PayloadVariable:
    def __init__(self, name: str, info: str, owner: object = None):
        self.name = name
        self.info = info
        self.owner = owner
        self._loaded = False
        self.lib_module = None
        self._value = None
    

    @property
    def modInfo(self) -> str:
        if self.lib_module:
            return self.lib_module.Info
        else:
            return "[!!] MODULE NOT LOADED [!!]"

    @property
    def status(self) -> bool:
        return self._loaded
    
    @property
    def status_str(self) -> str:
        if self._loaded:
            return "LOADED"
        else:
            return "EMPTY"
    
    def addModule(self, module: object) -> None:
        self.lib_module = module
        self._loaded = True
    
    def loadValue(self, data: any) -> None:
        self._value = data
        
    
    def clear(self) -> None:
        self._value = None
        self.lib_module = None
        self._loaded = False
    
