
from random import choice, randint
from typing import Union

class RandomTemplate:
    def __init__(self, coder: object):
        self.coder = coder
        self._choice_random = "$random"

    def randomStr(self, database: Union[list, tuple, set], variable: str) -> str:
        if variable == self._choice_random:
            return choice(database)
        else:
            return variable
    
    def randomVersion(self, number_count: int, separator: str = ",", min_ver: int = 1, max_ver: int = 4) -> str:
        raw = []
        for _ in range(number_count):
            raw.append(str(randint(min_ver, max_ver)))
        version = str(separator).join(raw)
        return version
    



