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
    
    def ccmd(self, command: str, no_output: bool = False) -> None:
        command = self.master.correct_command(command)
        self.cmd(command, no_output)
    
    def compileMod(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        self.msg("msg", f"Start building: {raw_exe.FILE_NAME}.....", sender=self.name)
        self.msg("msg", "Start compiler...", sender=self.name)
        # for k,i in comp.conf.items():
        #     print(f"{k} -- {i}")

        self.compiler.start()
        self.buildRes(raw_exe, comp)
        match raw_exe.master_module.fileType:
            case "dll":
                self.compile_DLL(raw_exe, comp)
            case "lib":
                self.compile_LIB(raw_exe, comp)
            case _:
                self.compile_EXE(raw_exe, comp)
        
        self.msg("msg", "Stopping compiler...", sender=self.name)
        self.compiler.stop()
        return raw_exe

    
    def compile_DLL(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        commands = comp.conf.get("DLL_LIB")
        if not commands:
            self.msg("error", "[!!] ERROR: Missing Linker instructions. [!!]", sender=self.name)
            return raw_exe
        for cmd in commands:
            self.msg("dev", self.master.correct_command(cmd), sender=self.name)
            self.ccmd(cmd)
        self.msg("msg", "Building Complete", sender=self.name)
        return raw_exe


    def compile_LIB(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        commands = comp.conf.get("STATIC_LIB")
        if not commands:
            self.msg("error", "[!!] ERROR: Missing Linker instructions. [!!]", sender=self.name)
            return raw_exe
        for cmd in commands:
            self.msg("dev", self.master.correct_command(cmd), sender=self.name)
            self.ccmd(cmd)
        self.msg("msg", "Building Complete", sender=self.name)
        return raw_exe
    
    def compile_EXE(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        commands = comp.conf.get("COMPILER_CMD")
        if not commands:
            self.msg("error", "[!!] ERROR: Missing Linker instructions. [!!]", sender=self.name)
            return raw_exe
        for cmd in commands:
            self.msg("dev", self.master.correct_command(cmd), sender=self.name)
            self.ccmd(cmd)
        self.msg("msg", "Building Complete", sender=self.name)
        return raw_exe
    
    def buildRes(self, raw_exe: RawExe, comp: RawCompiler) -> RawExe:
        if not comp.rc_script:
            return raw_exe
        cmd = comp.conf.get("BUILD_RES_OBJECT")
        if not cmd:
            self.msg("error", "[!!] ERROR: Missing command for RC Script. [!!]", sender=self.name)
            return raw_exe
        for c in cmd:
            self.msg("dev", self.master.correct_command(c), sender=self.name)
            self.ccmd(c)
        self.msg("msg", f"Building RES file: {comp.RES_OBJECT_FILE_NAME} complete.", sender=self.name)
        return raw_exe
        