import base64

from typing import Union
from .digdug import DigDug

class Shadow:
    def __init__(self, queen: object, worm_constructor: object):
        self.queen = queen
        self.msg = self.queen.msg
        self.WC = worm_constructor
        self.name = self.WC.name
    

    def use(self, raw_mod: object, raw_worm: object) -> Union[str, None]:
        match raw_mod.Name:
            case "DigDug":
                dd = DigDug()
                return "import base64\n" + dd.shadow(raw_worm.src_code, raw_worm.VAR)
            case "B64Py":
                return self.encode_b64(raw_worm.src_code, raw_worm.VAR.get("B64_exec"))
            case _:
                self.msg("error", f"[!!] ERROR: Shadow: '{raw_mod.Name}' does not exists [!!]", self.name)
                return None
    


    
    def encode_b64(self, code: str, executor: str) -> str:
        try:
            ecode = base64.b64encode(code.encode("utf-8"))
        except Exception as e:
            self.msg("error", f"[!!] ERROR encoding base64: {e} [!!]", sender=self.name)
            return ""
        if executor == "True" or executor == True or executor == "true":
            return f"import base64\nexec(base64.b64decode({ecode}).decode('utf-8'))"
        else:
            return str(ecode)
