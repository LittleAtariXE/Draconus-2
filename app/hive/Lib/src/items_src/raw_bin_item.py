import os
from typing import Union
from .raw_lib_item import RawLibItem


class RawBinItem(RawLibItem):
    def __init__(self, raw_info_item: object):
        super().__init__(raw_info_item)
        self._opt = raw_info_item._opt
 

        # A special type for handling binary files. #   'binType' 
        # binType##True
        self.binType = True

        # Name of binary file in the library
        self.binName = None


    @property
    def absFilePath(self) -> Union[str, None]:
        if not self.binName:
            return None
        return os.path.join(self._opt["BINARY_DIR"], self.binName)

    
    @property
    def raw_code(self) -> bytes:
        return self._load_code()

    def _load_code(self) -> bytes:
        try:
            with open(self.absFilePath, "rb") as file:
                data = file.read()
            return data
        except:
            return b""
    


