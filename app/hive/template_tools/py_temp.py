from typing import Union


class PyTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

    def makeModulesDict(self, modules_list: list) -> str:
        code = "{"
        for mod in modules_list:
            code += f"'{mod}' : {mod},"
        code += " }"
        return code
    
    def buildSortString(self, list_of_list: list, add_char: str = "") -> str:
        database = set()
        for li in list_of_list:
            for l in li:
                if l.startswith(add_char):
                    database.add(l)
                else:
                    database.add(f"{add_char}{l}")
        
        data = " ".join(list(database))
        return data
    
    def encodeHex(self, data: Union[str, bytes], encode: str = "utf-8") -> str:
        if isinstance(data, str):
            data = data.encode(encode)
        return str(data.hex())
    
    def buildLoader(self, script: str, loader: str, replace_char: str = "$") -> str:
        exe_script = loader.replace(replace_char, script)
        return exe_script
    

