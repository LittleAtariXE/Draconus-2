import os

from .mods.local_msg import LocalMSG
from .mods.py_pip_lib import PYTHON_PIP_LIBRARY_LINUX, PYTHON_PIP_LIBRARY_WINDOWS
from .Lib.library import Library
from .raw_worm_builder import RawWormBuilder
from .coder import Coder
from .worm_construtor import WormConstructor
from .compilers.master_compiler import MasterCompiler


# HIVE_MAIN_DIR = os.path.dirname(__file__)

class Queen:
    def __init__(self, builder_object: object):
        self.conf = builder_object

        self.DEV_MODE = self.conf.dev_mode
        self.DIR_HIVE = self.conf.DIR_HIVE
        self.DIR_HIVE_OUTPUT = self.conf.DIR_HIVE_OUT
        self.DIR_LIB_MAIN = os.path.join(self.DIR_HIVE, "Lib")
        self.DIR_ICONS = os.path.join(self.DIR_LIB_MAIN, "icons")
        self.PYTHON_PIP_LIBRARY_LINUX = PYTHON_PIP_LIBRARY_LINUX
        self.PYTHON_PIP_LIBRARY_WINDOWS = PYTHON_PIP_LIBRARY_WINDOWS
        self.DEFAULT_COMPILER_CORE = self.conf.DEFAULT_COMPILER_CORE
        self.msg = LocalMSG(self)

    
    @property
    def wormName(self) -> str:
        return self.rawBuilder.wormName

    def enter(self) -> None:
        self.library = Library(self)
        self.library.findItems()
        self.rawBuilder = RawWormBuilder(self, self.library)
        self.coder = Coder(self, self.rawBuilder)
        self.master_compiler = MasterCompiler(self)
        self.master_compiler.mountCore()
        self.wormConstructor = WormConstructor(self, self.rawBuilder, self.coder, self.master_compiler)
        
    

    def setWormName(self, name: str) -> None:
        self.rawBuilder.setWormName(name)
    
    def addWormIcon(self, name: str) -> None:
        self.rawBuilder.setIcon(name)
    
    def showIconList(self) -> None:
        self.rawBuilder.showIconList()
    
    def wormReset(self) -> None:
        self.rawBuilder.resetWorm()
    
    def showItems(self, item_type: str) -> None:
        self.library.showItem(item_type)
    
    def addWormItem(self, item_type: str, item_name: str) -> None:
        self.rawBuilder.Add(item_type, item_name)
    
    def removeWormItem(self, item_type: str, item_name: str) -> None:
        self.rawBuilder.removeWormItem(item_type, item_name)
    
    def setVariable(self, var_name: str, value: any, val_types: str = "str") -> None:
        self.rawBuilder.setVariable(var_name, value, val_types)
    
    def addFoodAsVar(self, target_var_name: str, food_name: str) -> None:
        self.rawBuilder.addFoodAsVar(target_var_name, food_name)
    
    def wormShow(self, params: list = None) -> None:
        self.rawBuilder.showWorm()
    
    def buildWorm(self, options: dict = {}) -> None:
        self.wormConstructor.buildWorm(options=options)

    def scanItems(self) -> None:
        self.library.findItems()
    
    def installCore(self) -> None:
        self.master_compiler.installCore()

    def test(self) -> None:
        self.enter()
        self.msg("msg", "Test HIVE")

    def Run(self) -> None:
        self.enter()
        





