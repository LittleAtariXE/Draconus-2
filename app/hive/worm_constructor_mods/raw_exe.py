from __future__ import annotations
import os
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..worm_construtor import WormConstructor
    from .master_raw import MasterRaw


class RawExe:
    def __init__(self, worm_constructor: WormConstructor, master_raw: MasterRaw, master_raw_lib_module: object, hive_type: str = None, output_file_type: str = "exe"):
        self.objType = "RawExe"
        self.hiveType = hive_type
        self.WC = worm_constructor
        self.master_raw = master_raw
        self.master_module = master_raw_lib_module
        self.VAR = self.master_raw.VAR
        self._output_file_type = output_file_type
        self.sort_modules = {
            "master" : [self.master_module],
            "child" : []
        }
        self._process_code = None

        # worm name
        if self.master_module.itemType == "worm":
            self.NAME = self.WC.RWB.wormName
        else:
            if self.master_module.modName:
                self.NAME = self.master_module.modName
            else:
                self.NAME = self.master_module.name
        
        # code language
        if self.master_module:
            if self.master_module.lang:
                self.code_lang = self.master_module.lang.lower()
        else:
            self.code_lang = None
        
        ### File path
        self.FILE_NAME = f"{self.NAME}{self.build_file_ext(self.master_module)}"
        self.fpath_dir_output = self.master_raw.dir_output
        self.fpath_src_file = os.path.join(self.fpath_dir_output, self.FILE_NAME)

        self.DIR_OUTPUT_NAME = self.master_raw.dir_output

        ### Module Process
        self.module_process = self.buildModProcess(self.master_module.modProcess)

        ### Compiler
        self.raw_compiler = None

        ### Final Output file
        self.final_output_name = f"{self.NAME}.{self._output_file_type}"
        self.final_output_fpath = os.path.join(self.fpath_dir_output, self.final_output_name)
        self.final_bin_path = None

        ### Shellcodes
        

        ### DLL
        self.dll_def_func = self._collect_def_func()
        self.dll_def_file_name = f"{self.NAME}.def"
        self.dll_def_file_path = os.path.join(self.fpath_dir_output, self.dll_def_file_name)
        self.dll_entry_point = "-Wl,--entry=DllMain"
        
        ### LOGS
        self.last_error = 0
        self.last_process_name = None
        self.last_process_error = ""



  

    @property
    def compilerItem(self) -> Union[object, None]:
        if self.master_module == self.master_raw.worm_master:
            return self.master_raw.worm_master_compiler
        else:
            return self.master_raw.RWB.wormGetModCompiler(self.master_module.name)
    
    @property
    def modules(self) -> list:
        mods = []
        for mod in self.sort_modules["child"]:
            mods.append(mod)
        for mod in self.sort_modules["master"]:
            mods.append(mod)
        return mods
    
    @property
    def MASTER_WORM(self) -> RawExe:
        return self.master_raw.worm_MASTER
    
    @property
    def linkerRequiredFiles(self) -> list:
        return self._check_req_files()
    
    @property
    def addToModuleCompilerCMD(self) -> list:
        return self._check_req_modules()
    
    @property
    def addToMainCompilerCMD(self) -> Union[list, None]:
        return self._add_to_main_comp_cmd()
    
    @property
    def is_readyApp(self) -> bool:
        if self.master_module.itemType == "worm":
            return True
        return self.master_module.readyApp
    


    def _add_to_main_comp_cmd(self) -> Union[list, None]:
        if self.master_module.addExeComp:
            return [self.final_output_name]
        else:
            return None



        
    def addRawModule(self, module: object, types: str = "child") -> None:
        self.sort_modules[types].append(module)
    
    def _check_req_modules(self) -> list:
        crm = set()
        for raw in self.master_raw.allRawExe:
            if raw.master_module.owner == self.master_module:
                if raw.master_module.addNameComp:

                    crm.add(raw.final_output_name)
        return list(crm)
    
    def _check_req_files(self) -> list:
        crf = set()
        for mod in self.modules:
            if mod.addNameComp:
                name = self.master_module.inFile.get(mod.name)
                if not name:
                    crf.add(mod.name)
                else:
                    crf.add(name)
        return list(crf)
    

        
    
    def build_file_ext(self, module: object) -> str:
        match module.lang.lower():
            case "nasm":
                ext = ".asm"
            case "python":
                ext = ".py"
            case "c":
                ext = ".c"
            case "cpp":
                ext = ".cpp"
            case "c++":
                ext = ".cpp"
            case _:
                ext = ""
        return ext
    
    def buildModProcess(self, process_list: list) -> list:
        modProc = []
        for pr in process_list:
            proc = self.WC.addProcessStep(pr)
            modProc.append(proc)
        return modProc
    
    ############## PAYLOADS ###############################

    @property
    def processCode(self) -> any:
        if not self._process_code:
            return self.master_module.raw_code
        else:
            return self._process_code
    
    def updateProcessCode(self, data: any):
        if isinstance(data, str):
            self._process_code = data.lstrip("\n")
        else:
            self._process_code = data

    ################### UPDATE ##########################
    # Automatic updating of variables, parameters, etc.

    def update(self) -> None:
        # update variable python worm module list
        for mod_name in self.sort_modules["child"]:
            if mod_name.fileType == "PY_MOD":
                self.VAR["_PY_MODULES"].append(mod_name.name)
            
    
    def _collect_def_func(self) -> list:
        def_func = []
        for mod in self.modules:
            def_func.extend(mod.dllDef)
        return def_func




# class RawExe:
#     def __init__(self, worm_constructor: WormConstructor, master_raw: MasterRaw, module_list: list, hive_type: str = None, output_file_type: str = "exe"):
#         self.objType = "RawExe"
#         self.hiveType = hive_type
#         self.WC = worm_constructor
#         self.master_raw = master_raw
#         self.modules = module_list
#         self.VAR = self.master_raw.VAR
#         self._output_file_type = output_file_type
#         self.master_module = self.modules[0]
        

#         # worm name
#         if self.master_module.itemType == "worm":
#             self.NAME = self.WC.RWB.wormName
#         else:
#             if self.master_module.modName:
#                 self.NAME = self.master_module.modName
#             else:
#                 self.NAME = self.master_module.name
        
#         # code language
#         if self.master_module:
#             self.code_lang = self.master_module.lang
#         else:
#             self.code_lang = None
        
        

#         ### File path
#         self.FILE_NAME = f"{self.NAME}{self.build_file_ext(self.master_module)}"
#         self.fpath_dir_output = self.master_raw.dir_output
#         self.fpath_src_file = os.path.join(self.fpath_dir_output, self.FILE_NAME)

#         ### INCLUDE FILES
#         self.include_files = []


#         ### Source code file
#         # dict ( file_path : code )
#         self.source_files = {}

#         ### Module Process
#         self.module_process = self.buildModProcess(self.master_module.modProcess)


#         ### LOGS
#         self.last_error = 0
#         self.last_process_name = None
#         self.last_process_error = ""

#     @property
#     def MASTER_WORM(self) -> RawExe:
#         return self.master_raw.worm_raw_child_master
    
#     @property
#     def compilerCMD(self) -> list:
#         return self._extra_compiler_command()
    
#     @property
#     def addToCompilerCmd(self) -> bool:
#         return self.master_module.addNameComp
    
#     def build_file_ext(self, module: object) -> str:
#         match module.lang.lower():
#             case "nasm":
#                 ext = ".asm"
#             case "python":
#                 ext = ".py"
#             case "c":
#                 ext = ".c"
#             case "cpp":
#                 ext = ".cpp"
#             case "c++":
#                 ext = ".cpp"
#             case _:
#                 ext = ""
#         return ext
    
#     def _extra_compiler_command(self) -> list:
#         cmd = []
#         for mod in self.modules:
#             if mod.addNameComp:
#                 if mod.supportFileCodeName:
#                     cmd.append(mod.supportFileCodeName)
#                 else:
#                     cmd.append(mod.name)
#         return cmd

#     def buildModProcess(self, process_list: list) -> list:
#         modProc = []
#         for pr in process_list:
#             proc = self.WC.addProcessStep(pr)
#             modProc.append(proc)
#         return modProc