
import ast
from typing import Union

DEFAULT_EMPTY_VALUE = "NO_VALUE"
DEFAULT_SHOW_VARIABLE_LIMIT = 20

class WormVariable:
    def __init__(self,
            name: str,
            info: str,
            owner: object = None,
            value: any = DEFAULT_EMPTY_VALUE,
            types: str = "str",
            options: dict = {}):
        
        self.name = name
        self.info = info
        self.owner = owner
        self.types = types
        self.options = options

        self.__first_value = value
        self.__value = value
        self.show_limit = DEFAULT_SHOW_VARIABLE_LIMIT
    
    @property
    def value(self) -> any:
        return self.convert_value(self.__value)
    

    def _convert2int(self, value: str) -> Union[str, int]:
        try:
            return int(value)
        except ValueError:
            return value
    
    def _convert_var(self, value: str) -> any:
        try:
            out = ast.literal_eval(value)
            return out
        except:
            return value
    
    def convert_value(self, raw_val: str) -> any:
        match self.types:
            case "str":
                return raw_val
            case "int":
                return self._convert2int(raw_val)
            case "list":
                return self._convert_var(raw_val)
            case _:
                return raw_val
    
    def show_value(self, max_limit: bool = True) -> str:
        if not max_limit:
            return str(self.__value)
        if len(str(self.__value)) > self.show_limit:
            return str(self.__value[0:self.show_limit])
        else:
            return str(self.__value)
    
    def set_value(self, value: any, val_type: str = None) -> None:
        self.__value = value
        if val_type:
            self.types = val_type
    
    def restore(self) -> None:
        self.__value = self.__first_value
    


