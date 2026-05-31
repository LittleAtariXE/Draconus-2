from typing import Union

class ItemOwner:
    def __init__(self):
        self._owners = []
    

    def add_owner(self, module: object) -> None:
        if module in self._owners:
            return
        else:
            self._owners.append(module)
    
    def return_owners(self) -> list:
        return self._owners
    
    def return_owner(self) -> Union[object, None]:
        if len(self._owners) == 0:
            return None
        else:
            return self._owners[0]
    
    
    
