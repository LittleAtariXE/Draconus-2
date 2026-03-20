import os


class PipExtraLibrary:
    def __init__(self, master_compiler: object):
        self.MC = master_compiler
        self.msg = self.MC.msg
        self.main_dir = os.path.dirname(__file__)
        self.extra_lib_path = os.path.join(self.main_dir, "pip_extra_lib.txt")
        self.PIP = self.load_extra()
        
    
    def load_extra(self) -> list:
        try:
            with open(self.extra_lib_path, "r") as file:
                rdata = file.read()
        except Exception as e:
            self.msg("error", f"[!!] ERROR: Load extra PIP library. Error: {e} [!!]", sender=self.MC.name)
            return []
        data = []
        for r in rdata.split("\n"):
            if r.startswith("#") or r == "\n" or r == "":
                continue
            data.append(r.strip())
        return data
