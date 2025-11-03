import base64


class PyBase64:
    def __init__(self, worm_constructor: object):
        self.wc = worm_constructor
        self.msg = self.wc.msg
        self.name = self.wc.name
    

    def encode_base64(self, code: str, add_executor: bool = True) -> str:
        try:
            en_code = base64.b64encode(code.encode("utf-8"))
        except Exception as e:
            self.msg("error", f"[!!] ERROR Decode module code: {e} [!!]", sender=self.name)
            return code
        
        if add_executor:
            en_code = f"import base64\nexec(base64.b64decode({en_code}).decode('utf-8'))"
        else:
            en_code = str(en_code)
        return en_code
    

    def PROCESS(self, code: str, var: dict = {}) -> str:
        return self.encode_base64(code)
