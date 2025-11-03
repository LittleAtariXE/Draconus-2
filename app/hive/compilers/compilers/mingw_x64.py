from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...worm_constructor_mods.raw_compiler import RawCompiler
    from ...worm_constructor_mods.raw_exe import RawExe
    from ..core.multi_comp import CrossCompCore
    from ..master_compiler import MasterCompiler




class MinGW_X64:
    def __init__(self, core: CrossCompCore, master_compiler: MasterCompiler):
        self.name = "MinGW_X64"
        self.core = core
        self.master = master_compiler
        self.msg = self.master.msg
        self.ecmd = self.core.eCMD
        self.compiler = self.core.compiler

        self.DIR_WORK_OUT = self.core.DOCKER_DIR_HIVE
    
    def compileEXE(self, cmd: dict, enter_dir: str) -> None:
        self.msg("dev", cmd["COMPILER_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["COMPILER_CMD"]}')
        self.msg("dev", cmd["LINKER_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["LINKER_CMD"]}')
        self.ecmd(f'{enter_dir} chmod 777 *')
    
    def compileStaticLIB(self, cmd: dict, enter_dir: str) -> None:
        self.msg("dev", cmd["COMPILER_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["COMPILER_CMD"]}')
        self.msg("dev", cmd["LINKER_LIB_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["LINKER_LIB_CMD"]}')
        self.ecmd(f'{enter_dir} chmod 777 *')
    
    # def compileDynamicLIB(self, raw_exe: RawExe, comp: RawCompiler) -> None:
    #     self.msg("msg", f"Build Dynamic Library: {raw_exe.FILE_NAME}....", sender=self.name)
    
    def compileDynamicLib(self, cmd: dict, enter_dir: str) -> None:
        self.msg("dev", cmd["COMPILER_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["COMPILER_CMD"]}')
        self.msg("dev", cmd["LINKER_DLL_CMD"], sender=self.name)
        self.ecmd(f'{enter_dir} {cmd["LINKER_DLL_CMD"]}')
        self.ecmd(f'{enter_dir} chmod 777 *')
    
    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start compilation: {raw_exe.FILE_NAME}....", sender=self.name)
        enter_dir = f"cd {self.DIR_WORK_OUT}/{comp.conf['__MASTER_WORM_NAME']} &&"
        self.msg("msg", "Start compiler....", sender=self.name)
        self.compiler.start()
        match raw_exe.master_module.fileType:
            case "lib":
                self.compileStaticLIB(comp.conf, enter_dir)
            case "dll":
                self.msg("msg", f"Compile Dynamic Library: {raw_exe.final_output_name}", sender=self.name)
                self.compileDynamicLib(comp.conf, enter_dir)
            case _:
                self.compileEXE(comp.conf, enter_dir)
        self.msg("msg", "Compile Done.", sender=self.name)
        self.msg("msg", "Stopping compiler....", sender=self.name)
        self.compiler.stop()
        return raw_exe
        