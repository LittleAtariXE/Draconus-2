


class PyTemplate:
    def __init__(self, coder: object):
        self.coder = coder
    

    def makeModulesDict(self, modules_list: list) -> str:
        code = "{"
        for mod in modules_list:
            code += f"'{mod}' : {mod},"
        code += " }"
        return code