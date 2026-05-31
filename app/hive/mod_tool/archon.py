

class Archon:
    def __init__(self, mod_wrapper: object, worm_constructor: object):
        self.SHADOW_TYPE = "shellcode"
        self.EXTRA_PROCESS_STEP = ["COMPILE", "SCODE_EXTRACT"]
        self.wc = worm_constructor
        self.mod_wrapper = mod_wrapper
        self.msg = self.wc.msg
    

    def PROCESS(self, code: str, var: dict) -> str:
        code = self.wc.renderSingleTemplate(code, var)
        return code


