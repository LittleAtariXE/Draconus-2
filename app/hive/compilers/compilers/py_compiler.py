from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...worm_constructor_mods.raw_compiler import RawCompiler
    from ...worm_constructor_mods.raw_exe import RawExe
    from ..core.multi_comp import CrossCompCore
    from ..master_compiler import MasterCompiler


class PyCompiler:
    def __init__(self, core: CrossCompCore, master_compiler: MasterCompiler):
        self.name = "PyCompiler"
        self.core = core
        self.master = master_compiler
        self.msg = self.master.msg
        self.ecmd = self.core.eCMD
        self.compiler = self.core.compiler

        self.DIR_WORK_OUT = self.core.DOCKER_DIR_HIVE
    
    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start compilation: {raw_exe.FILE_NAME}....", sender=self.name)
        enter_dir = f"cd {self.DIR_WORK_OUT}/{comp.conf['__MASTER_WORM_NAME']} &&"
        print(comp.conf)
        self.msg("msg", "Start compiler....", sender=self.name)
        self.compiler.start()
        self.msg("dev", comp.conf["COMPILER_CMD"], sender=self.name)
        self.ecmd(f"{enter_dir} {comp.conf['COMPILER_CMD']}")
        clean = comp.conf.get("COMPILER_CLEAN")
        if clean:
            for com in clean:
                self.msg("dev", com, sender=self.name)
                self.ecmd(com)
        self.msg("msg", "Stopping compiler....", sender=self.name)
        self.compiler.stop()
        return raw_exe