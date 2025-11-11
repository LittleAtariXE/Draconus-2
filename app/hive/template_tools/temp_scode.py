

from typing import Union


class ShellTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

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
