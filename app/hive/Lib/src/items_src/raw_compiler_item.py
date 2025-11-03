
from .raw_lib_item import RawLibItem

class RawCompilerItem(RawLibItem):
    def __init__(self, raw_info_item: object):
        super().__init__(raw_info_item)

        # compiler core
        self.compilerCore = None

        # compiler_data
        self.compilerData = None

        # 'compiler item name' in Master Compiler
        # The name of the compiler that the 'master compiler' will use
        self.compilerMCNAME = None
    