


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