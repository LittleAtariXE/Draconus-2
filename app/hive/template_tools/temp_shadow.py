import string
from random import choice
from typing import Union


class ShadowTemplate:
    def __init__(self, coder: object):
        self.coder = coder
        self.__shadow_table = None

        self.LAYER_CHAR_DEFAULT = string.ascii_letters + string.digits + "_" + "." + " " + ":" + "%" + '"' + "-"

    
    @property
    def SHADOW_TABLE(self) -> Union[dict, None]:
        if self.__shadow_table:
            return self.__shadow_table
        else:
            return None


    def MakeTable(self, data: str, base_chars: str = None) -> dict:
        if not base_chars:
            base_chars = self.LAYER_CHAR_DEFAULT
        chars = {}
        for char in base_chars:
            chars[char] = []
        base = list(data)
        for index, char in enumerate(base):
            if not char in chars.keys():
                continue
            chars[char].append(index)
        self.__shadow_table = chars
        return chars
    
    def DigitsEncode(self, text: str, add_zero: bool = True) -> str:
        # Copies text into the form of indexes to the text placed in 'SHADOW TABLE'
        if not self.SHADOW_TABLE:
            return "0"
        code = []
        for char in text:
            if not char in self.SHADOW_TABLE.keys():
                continue
            code.append(str(choice(self.SHADOW_TABLE[char])))
        if add_zero:
            code.append("0")
        return ", ".join(code)
    
    def DigitsEncode2(self, text: str, obf_chars: dict, add_zero: bool = True) -> str:
        code = []
        for char in text:
            if not char in obf_chars.keys():
                continue
            code.append(str(choice(obf_chars[char])))
        if add_zero:
            code.append("0")
        return ", ".join(code)
    
    def BuildAsmVariables(self, var_name: str, text_data: str, var_len_limit: int = 1024) -> str:
        # Building the ASM code that contains the text used to create the SHADOW TABLE
        data = [text_data[i:i+var_len_limit] for i in range(0, len(text_data), var_len_limit)]
        single_var_code = ""
        sum_var_code = f"{var_name}_all dq"
        for i, d in enumerate(data):
            single_var_code += f'{var_name}{i}: db "{d}", 0\n'
            sum_var_code += f' {var_name}{i},'
        # add empty 
        single_var_code += f'{var_name}{i+1}: db "", 0\n'
        sum_var_code += f' {var_name}{i+1},'
        sum_var_code += "0"
        code = single_var_code + "\n" + sum_var_code + "\n"
        return code
    
    def DaleBuildKey(self, key: str) -> list:
        nkey = []
        for k in key:
            nkey.append(ord(k))
        return nkey
    
    def DaleKey(self, key: Union[str, list], add_zero: bool = True) -> str:
        if isinstance(key, str):
            key = self.DaleBuildKey(key)
        hkey = []
        for k in key:
            hkey.append(f"{hex(k)}")
        if add_zero:
            hkey.append("0x00")
        return ", ".join(hkey)
    
    def DaleShadow(self, text: str, key: Union[str, list], add_zero: bool = True) -> str:
        if isinstance(key, str):
            key = self.DaleBuildKey(key)
        etext = []
        i = 0
        for raw in text:
            if i == len(key):
                i = 0
            etext.append(ord(raw) + key[i])
            i += 1
        enc = []
        for et in etext:
            enc.append(f"{hex(et)}")
        if add_zero:
            enc.append("0x00")
        return ", ".join(enc)

    def ShadowTextRR(self, text: str, key: Union[str, list], add_zero: bool = True) -> str:
        if isinstance(key, str):
            key = [ord(k) for k in key]
        i = 0
        data = []
        for c in text:
            if i == len(key):
                i = 0
            data.append(hex(ord(c) * key[i]))
            i += 1
        if add_zero:
            data.append("0x00")
        return ", ".join(data)

