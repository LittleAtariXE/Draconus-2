from .raw_lib_item import RawLibItem


class RawRcScript(RawLibItem):
    def __init__(self, raw_info: object):
        super().__init__(raw_info)


        # Specifies which compiler the script will be assigned to.
        self.compilerOwner = None
    




    def setCompilerOwner(self, raw_comp_item: object) -> None:
        self.compilerOwner = raw_comp_item
    
    