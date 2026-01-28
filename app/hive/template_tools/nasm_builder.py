
from typing import Union


class NasmBuilderTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

    def PutStackCode(self, code: str, registry: str = "rcx", bytes_len: int = 8, shadow_space_enter: int = 40, add_null: bool = True, add_tabulate: int = 1) -> tuple:
        ### Creates code that places data into a register and then onto the stack, 
        ### counts repeated stack pushes, and returns a tuple containing the code and the value for "sub rsp".
        ## ex: mov rcx, 0x1234567890
        ##     push rcx
        ################################################################################
        ####### RETURN tuple:
        ####### (code, shadow_space_enter, shadow_space_exit)
        tab = "\t" * add_tabulate
        data = []
        for n in range(0, len(code), bytes_len):
            data.append(code[n:n+bytes_len][::-1])
        ascii_data = []
        for d in reversed(data):
            ascii_data.append(d.encode("ascii").hex())
        if len(ascii_data[0]) == bytes_len * 2 and add_null:
            ascii_data.insert(0, "00")
        while len(ascii_data[0]) < bytes_len * 2:
            ascii_data[0] = "00" + ascii_data[0]
        # shadow space
        ss_exit = len(ascii_data) * 8
        if ss_exit & 8 == 0:
            ss_enter = shadow_space_enter
        else:
            ss_enter = shadow_space_enter + 8
        ss_exit += ss_enter
        code = ""
        for line in ascii_data:
            code += f"{tab}mov {registry}, 0x{line}\n"
            code += f"{tab}push {registry}\n"

        return (code, ss_enter, ss_exit)
    
    def ConvertHexBytes(self, data: str, add_null: bool = True, separator: str = ", ") -> str:
        # convert data to hex bytes
        # 0x10, 0x20, 0x3a etc.
        hex_data = [f"0x{ord(one_byte):02X}" for one_byte in data]
        if add_null:
            hex_data.append("0x00")
        out = separator.join(hex_data)
        return out
    
    def ConvertHexBytesPart(self, data: str, add_null: bool = True, part_len: int = 1024, encrypt_byte: int = 0, tabs: int = 1) -> str:
        tabs = "\t" * tabs
        hex_data = [f"0x{ord(obyte) + encrypt_byte:02X}" for obyte in data]
        if add_null:
            hex_data.append("0x00")
        code = ""
        for i in range(0, len(hex_data) - 1, part_len):
            code += f"{tabs} db "
            code += ", ".join(hex_data[i:i+part_len])
            code += "\n"
        return code
