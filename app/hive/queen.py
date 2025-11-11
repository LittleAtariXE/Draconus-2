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

        self.DIR_HIVE = self.conf.DIR_HIVE
        self.DIR_HIVE_OUTPUT = self.conf.DIR_HIVE_OUT
        self.DIR_LIB_MAIN = os.path.join(self.DIR_HIVE, "Lib")
        self.DIR_ICONS = os.path.join(self.DIR_LIB_MAIN, "icons")
        self.PYTHON_PIP_LIBRARY_LINUX = PYTHON_PIP_LIBRARY_LINUX
        self.PYTHON_PIP_LIBRARY_WINDOWS = PYTHON_PIP_LIBRARY_WINDOWS
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

    def test(self) -> None:
        self.msg("msg", "Test HIVE")
        conf = {}





        #conf["FLAG_NO_COMPILE"] = True
        # conf["BUILD_PAYLOAD"] = True
        # conf["MODULE_INFO"] = "My first shellcode FOOD."
        #conf["BUILD_SHELLCODE_PAYLOAD"] = True
        # conf["BUILD_SHELLCODE_FOOD"] = True


        self.addWormItem("worm", "Montezuma")
        # self.addWormItem("rscript", "BasicRes")


        self.wormShow()
        #self.buildWorm()
        
        #self.master_compiler.coreInstall("CrossCompCore")
        # self.rawBuilder.setWormName("kurwinox")
        # self.rawBuilder.Add("worm", "WShellcode")
        # self.rawBuilder.Add("scode", "MsgBoxA")



        # self.rawBuilder.Add("worm", "PyScode")
        # self.rawBuilder.addFoodAsVar("szelkod", "FSzel")
        # self.rawBuilder.Add("module", "AkMod")
        # self.rawBuilder.removeWormItem("module", "AkMod")
        # self.rawBuilder.Add("worm", "Kapelusz")
        # self.rawBuilder.Add("payload", "EvilPay")
        # self.rawBuilder.removeWormItem("compiler", "PyInstaller")
        #self.rawBuilder.removeWormItem("payload", "EvilPay")
        #self.rawBuilder.Add("scode", "MsgBoxA")
        # self.rawBuilder.Add("rscript", "BasicRes")
        # self.rawBuilder.setIcon("worm1.ico")
        #self.rawBuilder.Add("payload", "PyRevTcp")
        # self.rawBuilder.Add("scode", "MsgBoxA")
        #self.rawBuilder.Add("worm", "Asmek")
        # self.rawBuilder.Add("worm", "Montezuma")
        # self.rawBuilder.Add("module", "PyRawTcp")
        # self.rawBuilder.Add("shadow", "DigDug")
        # self.rawBuilder.addFoodAsVar("Ktext", "CharFood")
        # self.rawBuilder.Add("worm", "Pajtek")
        # self.rawBuilder.Add("module", "PajMod")
        # self.rawBuilder.Add("payload", "EvilPay")
        # self.rawBuilder.Add("compiler", "MinGW_x64_Nasm", "Asmek")
        #self.rawBuilder.Add("worm", "MultiTest")
        #self.rawBuilder.Add("module", "NasmMod")

        # self.rawBuilder.test()
        # self.rawBuilder.showWorm()
        # self.wormConstructor.buildWorm(options=conf)

    
        



    def Run(self) -> None:
        self.enter()
        self.test()





