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
        self.rc_script = self.raw_exe.rcScript

        self.RC_SCRIPT_FILE_NAME = f"{self.raw_exe.NAME}.rc"
        self.RES_OBJECT_FILE_NAME = f"{self.raw_exe.NAME}.res"


        self.conf = self._buildBasicCompilerVar()
    
    @property
    def raw_code(self) -> str:
        return self.comp_item.raw_code
    
    @property
    def MC_compiler(self) -> Union[str, None]:
        return self.comp_item.compilerMCNAME
    
    @property
    def RC_script_fpath(self) -> Union[str, None]:
        if not self.rc_script:
            return None
        else:
            return os.path.join(self.raw_exe.fpath_dir_output, self.RC_SCRIPT_FILE_NAME)

    
    def _buildBasicCompilerVar(self) -> dict:
        cvar = {}
        if self.raw_exe.wormIcon:
            cvar["__ICON_NAME"] = self.raw_exe.master_raw.worm_icon
        else:
            cvar["__ICON_NAME"] = None
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
        cvar["__DEFAULT_DLL_LIST"] = self.raw_exe.master_raw.DEFAULT_LINKER_DLL_LIST
        cvar["__LINKER_EXTRA_FILE"] = self.raw_exe.linkerRequiredFiles
        cvar["__LINKER_EXTRA_FILE_STR"] = " ".join(cvar["__LINKER_EXTRA_FILE"])
        cvar["__VAR_EXEC_SHOW"] = self.raw_exe.VAR.get("EXEC_SHOW")
        if self.rc_script:
            cvar["__BUILD_RC"] = True
            cvar["__RC_SRC_FILE_NAME"] = self.RC_SCRIPT_FILE_NAME
            cvar["__RC_OUTPUT_FILE_NAME"] = self.RES_OBJECT_FILE_NAME
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




    
