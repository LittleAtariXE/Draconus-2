from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ..mods.py_pip_lib import PYTHON_PIP_LIBRARY_LINUX, PYTHON_PIP_LIBRARY_WINDOWS
from .core.multi_comp import CrossCompCore
from .compilers.mingw_x64 import MinGW_X64
from .compilers.py_compiler import PyCompiler


if TYPE_CHECKING:
    from ..queen import Queen
    from ..worm_constructor_mods.raw_exe import RawExe
    from ..worm_constructor_mods.raw_compiler import RawCompiler




class MasterCompiler:
    def __init__(self, queen: Queen):
        self.name = "MasterCompiler"
        self.queen = queen
        self.msg = self.queen.msg
        self.cores = {}
        self.compilers = {}


        self.DIR_HIVE_OUT = self.queen.DIR_HIVE_OUTPUT
        self.DIR_HIVE_IN_DOCKER = self.queen.conf.DIR_HIVE_IN_DOCKER_IMAGE
        self.PYTHON_PIP_LIBRARY_LINUX = PYTHON_PIP_LIBRARY_LINUX
        self.PYTHON_PIP_LIBRARY_WINDOWS = PYTHON_PIP_LIBRARY_WINDOWS
    
    def mountCore(self) -> None:
        CC_core = CrossCompCore(self)
        if not CC_core.status:
            self.msg("error", f"WARNING: Cross Compiler Core is not installed.", sender=self.name)
        self.cores["CrossCompCore"] = CC_core
        mingwx64 = MinGW_X64(CC_core, self)
        self.compilers["MinGW_X64"] = mingwx64
        pycomp = PyCompiler(CC_core, self)
        self.compilers["PyComp"] = pycomp

    
    def startCompile(self, raw_exe: RawExe, mod_compiler: RawCompiler = None) -> RawExe:
        if not mod_compiler:
            mod_compiler = raw_exe.raw_compiler
            if not mod_compiler:
                self.msg("error", f"[!!] ERROR: The selected module does not have a compiler. [!!]", sender=self.name)
                raw_exe.last_error == 1
                raw_exe.last_process_error = "ERROR: The selected module does not have a compiler."
                return raw_exe
        self.msg("msg", f"Start compilation: {raw_exe.NAME} ...", sender=self.name)
        # check compiler
        mc_comp = self.compilers.get(mod_compiler.MC_compiler)
        if not mc_comp:
            self.msg("msg", f"[!!] ERROR: Compiler: '{mod_compiler.MC_compiler}' does not exists or not installed. [!!]", sender=self.name)
            raw_exe.last_error == 1
            raw_exe.last_process_error = f"[!!] ERROR: Compiler: '{mod_compiler.MC_compiler}' does not exists or not installed. [!!]"
            return raw_exe

        mc_comp.compileMod(raw_exe, mod_compiler)

        return raw_exe
    
    def coreInstall(self, core_name: str) -> None:
        core = self.cores.get(core_name)
        if not core:
            self.msg("error", f"[!!] ERROR: '{core_name}' does not exists. [!!]", sender=self.name)
            return
        core.installCore()
