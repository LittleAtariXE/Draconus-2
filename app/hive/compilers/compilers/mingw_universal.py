from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...worm_constructor_mods.raw_compiler import RawCompiler
    from ...worm_constructor_mods.raw_exe import RawExe
    from ..master_compiler import MasterCompiler



class MinGW_All:
    def __init__(self, core: object, master_compiler: MasterCompiler):
        self.name = "MinGW-x64"
        self.master = master_compiler
        self.msg = self.master.msg
        self.core = core
        self.cmd = self.core.eCMD
        self.compiler = self.core.compiler

        self.DIR_WORK_OUT = self.core.DOCKER_DIR_HIVE
    
    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start building: {raw_exe.FILE_NAME}.....", sender=self.name)
        match raw_exe.master_module.fileType:
            case _:
                self.compile_EXE(raw_exe, comp)

        return raw_exe
    
    def compile_EXE(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        commands = comp.conf.get("COMPILER_CMD")
        if not commands:
            self.msg("error", "[!!] ERROR: Missing Linker instructions. [!!]", sender=self.name)
            return raw_exe
        self.msg("msg", "Start compiler...", sender=self.name)
        self.compiler.start()
        for cmd in commands:
            self.msg("dev", cmd, sender=self.name)
            self.cmd(cmd)
        self.msg("msg", "Building Complete", sender=self.name)
        self.msg("msg", "Stopping compiler...", sender=self.name)
        self.compiler.stop()
        return raw_exe
        