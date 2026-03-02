from __future__ import annotations
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...worm_constructor_mods.raw_compiler import RawCompiler
    from ...worm_constructor_mods.raw_exe import RawExe
    from ..core.multi_comp import CrossCompCore
    from ..master_compiler import MasterCompiler


class ScExtrator:
    def __init__(self, core: object, master_compiler: MasterCompiler):
        self.name = "MinGW-SCode"
        self.master = master_compiler
        self.msg = self.master.msg
        self.core = core
        self.cmd = self.core.eCMD
        self.compiler = self.core.compiler

        self.DIR_WORK_OUT = self.core.DOCKER_DIR_HIVE
    
    def ccmd(self, command: str, no_output: bool = False) -> None:
        command = self.master.correct_command(command)
        self.cmd(command, no_output)

    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start compilation: {raw_exe.FILE_NAME}....", sender=self.name)
        cmd = comp.conf.get("COMPILER_CMD")
        if not cmd:
            self.msg("error", "[!!] ERROR: Missing Compiler instructions. [!!]", sender=self.name)
            return raw_exe
        self.msg("msg", "Start compiler....", sender=self.name)
        self.compiler.start()
        for c in cmd:
            self.msg("dev", c, sender=self.name)
            self.ccmd(c)
        scode = comp.conf.get("SCODE_EXTRACT")
        if not scode:
            self.msg("error", "[!!] ERROR: Missing shellcode extract commands. [!!]", sender=self.name)
            return raw_exe
        for sc in scode:
            self.msg("dev", sc, sender=self.name)
            self.ccmd(sc, True)
        raw_exe.final_bin_path = os.path.join(raw_exe.fpath_dir_output, f"{raw_exe.NAME}.o")
        self.msg("msg", "Compile Done.", sender=self.name)
        self.msg("msg", "Stopping compiler....", sender=self.name)
        self.compiler.stop()
        return raw_exe




class ShellCodeExtractor:
    def __init__(self, core: CrossCompCore, master_compiler: MasterCompiler):
        self.name = "MinGW_ShellcodeExtractor"
        self.core = core
        self.master = master_compiler
        self.msg = self.master.msg
        self.ecmd = self.core.eCMD
        self.compiler = self.core.compiler

        self.DIR_WORK_OUT = self.core.DOCKER_DIR_HIVE
    
    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start compilation: {raw_exe.FILE_NAME}....", sender=self.name)
        sc_extract = comp.conf.get("SHELLCODE_EXTRACT")
        if not sc_extract:
            self.msg("error", "[!!] ERROR: Compiler does not have a command to build shellcode. [!!]", sender=self.name)
            return raw_exe
        self.msg("msg", "Start compiler....", sender=self.name)
        self.compiler.start()
        self.msg("dev", str(sc_extract.get("COMPILER_CMD")), sender=self.name)
        self.ecmd(sc_extract.get("COMPILER_CMD"))
        self.msg("dev", str(sc_extract.get("SCODE_EXTRACT")), sender=self.name)
        self.ecmd(sc_extract.get("SCODE_EXTRACT"))
        raw_exe.final_bin_path = os.path.join(raw_exe.fpath_dir_output, f"{raw_exe.NAME}.o")
        clean_cmd = sc_extract.get("COMPILER_CLEAN")
        if clean_cmd:
            for cmd in clean_cmd:
                self.msg("dev", cmd, sender=self.name)
                self.ecmd(cmd)
        self.msg("msg", "Compile Done.", sender=self.name)
        self.msg("msg", "Stopping compiler....", sender=self.name)
        self.compiler.stop()
        return raw_exe