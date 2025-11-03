from __future__ import annotations
import json
import os
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .raw_exe import RawExe
    from ..worm_construtor import WormConstructor
    from ..Lib.src.items_src.raw_compiler_item import RawCompilerItem


class RawCompiler:
    def __init__(self, raw_exe: RawExe, compiler_item: RawCompilerItem):
        self.raw_exe = raw_exe
        self.comp_item = compiler_item
        self.conf = self._buildBasicCompilerVar()
    
    @property
    def raw_code(self) -> str:
        return self.comp_item.raw_code
    
    @property
    def MC_compiler(self) -> Union[str, None]:
        return self.comp_item.compilerMCNAME

    
    def _buildBasicCompilerVar(self) -> dict:
        cvar = {}
        cvar["__SRC_FILE_NAME"] = self.raw_exe.FILE_NAME
        cvar["__MODULE_NAME"] = self.raw_exe.NAME
        cvar["__FINAL_OUTPUT_FTYPE"] = self.raw_exe._output_file_type
        cvar["__FINAL_OUTPUT_FNAME"] = self.raw_exe.final_output_name
        cvar["__MASTER_WORM_NAME"] = self.raw_exe.master_raw.worm_name
        elib, elib_s = self._buildExtraLib()
        cvar["__EXTRA_LIBRARY"] = elib
        cvar["__EXTRA_LIBRARY_STR"] = elib_s
        cvar["__HIVE_DOCKER"] = self.raw_exe.master_raw.DIR_HIVE_IN_DOCKER
        cvar["__READY_APP_DOCKER"] = self.raw_exe.master_raw.DIR_READY_APP_IN_DOCKER
        cvar["__WORK_DIR_DOCKER"] = os.path.join(cvar["__HIVE_DOCKER"], cvar["__MASTER_WORM_NAME"])
        cvar["__DEF_FILE_NAME"] = self.raw_exe.dll_def_file_name
        cvar["__DLL_ENTRY_POINT"] = self.raw_exe.dll_entry_point
        return cvar
    
    def _buildExtraLib(self) -> tuple(list, str):
        libs = self.raw_exe.addToModuleCompilerCMD
        libs_str = " ".join(libs)
        return (libs, libs_str)
    
    def updateConfig(self, json_conf: str) -> bool:
        try:
            conf = json.loads(json_conf)
        except json.JSONDecodeError as e:
            self.raw_exe.last_error = 1
            self.raw_exe.last_process_error = f"ERROR: Decode JSON compiler configuration. Error: {e}"
            return False
        self.conf.update(conf)
        return True

# class RawCompiler:
#     def __init__(self, raw_exe: RawExe, compiler_item: RawCompilerItem):
#         self.raw_exe = raw_exe
#         self.raw_comp = compiler_item
#         self.conf = None

#         self.COMPILER_CMD = None

#     @property
#     def raw_code(self) -> str:
#         return self.raw_comp.raw_code
    
#     @property
#     def MC_compiler(self) -> Union[str, None]:
#         return self.raw_comp.compilerMCNAME

#     @property
#     def compilerVAR(self) -> dict:
#         cvar = {}
#         cvar["__SRC_FILE_NAME"] = self.raw_exe.FILE_NAME
#         cvar["__MODULE_NAME"] = self.raw_exe.NAME
#         cvar["__FINAL_OUTPUT"] = self.raw_exe._output_file_type
#         cvar["__MASTER_WORM_NAME"] = self.raw_exe.master_raw.worm_name
#         cvar["__EXTRA_LIBRARY"] = self.raw_exe.addToMainCompilerCMD
#         return cvar
    
#     def buildCMD(self, extra_conf: dict = {}) -> dict:
#         if not self.conf:
#             self.raw_exe.last_error == 1
#             self.raw_exe.last_process_error = "ERROR: Can't build compiler command. Missing compiler config."
#             return {}
#         self.conf.update(extra_conf)
#         self.conf["COMPILER"] = self._build_compiler_conf(self.conf)
#         self.conf["LINKER"] = self._build_linker_conf(self.conf)
#         self.COMPILER_CMD = self.conf
#         return self.conf
    
#     def loadConf(self, config: str) -> None:
#         try:
#             conf = json.loads(config)
#             self.conf = conf
#         except json.JSONDecodeError as e:
#             self.raw_exe.last_error = 1
#             self.raw_exe.last_process_error = f"ERROR: Decode config to compiler. ERROR: {e}"
#             self.conf = None
            
    
#     def build_cmd(self, extra_conf: dict = {}) -> dict:
#         if not self.conf:
#             self.raw_exe.last_error == 1
#             self.raw_exe.last_process_error = "ERROR: Can't build compiler command. Missing compiler config."
#             return
#         self.conf.update(extra_conf)
#         compiler_conf = {}
#         compiler_conf["COMPILER"] = self._build_compiler_conf(self.conf)
#         self.COMPILER_CMD = compiler_conf
#         return compiler_conf
    
#     def _build_compiler_conf(self, raw_conf: dict) -> dict:
#         conf = {}
#         conf["COMPILER_EXEC"] = raw_conf["COMPILER"].get("COMPILER_EXEC")
#         conf["SRC_FILE_NAME"] = raw_conf["COMPILER"].get("SRC_FILE_NAME")
#         conf["OUTPUT_RAW_FILENAME"] = self.conf["COMPILER"].get("OUTPUT_FILENAME")
#         conf["OUTPUT_RAW_FILETYPE"] = self.conf["COMPILER"].get("OUTPUT_FILETYPE")
#         if conf["OUTPUT_RAW_FILENAME"] and conf["OUTPUT_RAW_FILETYPE"]:
#             conf["OUTPUT_FILENAME"] = f'{conf["OUTPUT_RAW_FILENAME"]}{conf["OUTPUT_RAW_FILETYPE"]}'
#         else:
#             conf["OUTPUT_FILENAME"] = "Unknown"
        
#         return conf
    
    
    
#     def _build_linker_conf(self, raw_conf: dict) -> dict:
#         linker = raw_conf["LINKER"]
#         conf = {}
#         conf["COMPILER_EXEC"] = linker.get("COMPILER_EXEC")
#         conf["SRC_FILE_NAME"] = linker.get("SRC_FILE_NAME")
#         conf["NO_STD_LIB"] = linker.get("NO_STD_LIB")
#         conf["DEFAULT_DLL"] = linker.get("DEFAULT_DLL")
#         conf["EXTRA_LIB"] = self.raw_exe.compilerCMD
#         conf["OUTPUT_FILENAME"] = self.raw_exe.final_output_name
#         return conf


    
