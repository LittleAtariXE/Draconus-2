from __future__ import annotations
import os
import shutil
import json
from pathlib import Path
from typing import Union, Callable, TYPE_CHECKING, Optional
from collections import ChainMap

from .worm_constructor_mods.master_raw import MasterRaw
from .worm_constructor_mods.raw_compiler import RawCompiler
from .mod_tool.mod_wrapper import ModWrapper
if TYPE_CHECKING:
    from .raw_worm_builder import RawWormBuilder
    from .coder import Coder
    from .queen import Queen
    from .worm_constructor_mods.raw_exe import RawExe
    from .compilers.master_compiler import MasterCompiler


class WormConstructor:
    def __init__(self, queen: Queen, raw_worm_builder: RawWormBuilder, coder: Coder, master_compiler: MasterCompiler):
        self.name = "WormConstructor"
        self.queen = queen
        self.msg = self.queen.msg
        self.RWB = raw_worm_builder
        self.Coder = coder
        self.renderSingleTemplate = self.Coder.renderSingleTemplate
        self.masterCompiler = master_compiler
        self.SpecialModules = ModWrapper(self)

        self.DIR_OUTPUT = self.queen.DIR_HIVE_OUTPUT
        self.DIR_READY_APP_SUFFIX = "_ready"
        self.DIR_HIVE_IN_DOCKER_IMAGE = self.queen.conf.DIR_HIVE_IN_DOCKER_IMAGE
    

    def _build_options(self) -> dict:
        opt = {}
        opt["WORM_NAME"] = self.RWB.wormName
        opt["DIR_OUTPUT"] = os.path.join(self.DIR_OUTPUT, self.RWB.wormName)
        opt["DIR_READY_SUFFIX"] = self.DIR_READY_APP_SUFFIX
        return opt
    
    def _build_variables(self) -> dict:
        return self.Coder.buildVariable()
    
    def _prepare_dirs(self, master_raw: MasterRaw) -> bool:
        if not os.path.exists(master_raw.dir_output):
            try:
                os.mkdir(master_raw.dir_output)
            except Exception as e:
                self.msg("error", f"[!!] ERROR Making directory for worm: {e} [!!]", sender=self.name)
                return False
        
        if not os.path.exists(master_raw.dir_ready_app):
            try:
                os.mkdir(master_raw.dir_ready_app)
            except Exception as e:
                self.msg("error", f"[!!] ERROR Making ready worm directory: {e} [!!]", sender=self.name)
                return False
        
        return True
    
    def saveFile(self, fpath: str, data: str) -> bool:
        try:
            with open(fpath, "w") as file:
                file.write(data)
            return True
        except Exception as e:
            self.msg("error", f"[!!] ERROR Save file: {fpath}. {e} [!!]", sender=self.name)
            return False
    
    def loadCode(self, fpath: str) -> Union[str, None]:
        try:
            with open(fpath, "r") as file:
                data = file.read()
            return data
        except Exception as e:
            self.msg("error", f"[!!] ERROR Load code: {fpath}. {e} [!!]", sender=self.name)
            return None



    def buildWorm(self, module_list: list = None, options: dict = {}) -> None:
        self.msg("msg", f"  START BUILDING WORM: <<< {self.RWB.wormName} >>> ....   ", color="white", sender=self.name)
        ## build worm options
        opt = self._build_options()
        opt.update(options)
        #######
        worm_var = self._build_variables()
        master = MasterRaw(self, opt, worm_var)

        # making directory
        if not self._prepare_dirs(master):
            self.msg("error", "[!!] ABORT BUILDING PROCESS [!!]", sender=self.name)
            return
        





        # prepare worm process
        proc_list = self.prepareProcess(master.worm_process_step)
        master.worm_process_execute = proc_list
        master.worm_raw_child_master = self.executeProcessList(master.worm_MASTER, master.worm_process_execute)

        self.msg("msg", "Builiding complete", sender=self.name)


    
    def executeProcessList(self, raw_object: RawExe, process_list: list) -> object:
        for proc in process_list:
            #raw_object = proc(raw_object)
            proc(raw_object)
            self.msg("dev", f"Object: {raw_object.NAME} ## Process Name: {raw_object.last_process_name}", sender=self.name)
            # print(raw_object.NAME)
            # print(raw_object.last_process_name)
        return raw_object
        

    def prepareProcess(self, process_list: list) -> list:
        proc_list = []
        for pl in process_list:
            proc_list.append(self.addProcessStep(pl))
        return proc_list

    def addProcessStep(self, process_name: str) -> Callable:
        match process_name.lower():
            case "build_code":
                return self.process_BuildCode
            case "build_lib":
                return self.process_BuildStaticLib
            case "compile":
                return self.process_Compile
            case "done":
                return self.process_FinalStep
            case "payload":
                return self.process_BuildPayload
            case "shadow_code":
                return self.process_ShadowCode
            case _:
                return self.process_Empty

    
    def process_Empty(self, raw_object: Union[RawExe, MasterRaw]) -> Union[RawExe, MasterRaw]:
        raw_object.last_process_name = "Empty Process"
        return raw_object
    
    #################### BUILD CODE PROCESS ######################################

    def _build_nasm_raw_worm(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Build NASM Raw Worm"
        raw_code = self.Coder.buildNasmCode(raw_object.modules, raw_object.fpath_dir_output, raw_object.FILE_NAME)
        for fpath, rcode in raw_code.items():
            code = self.renderSingleTemplate(rcode, raw_object.VAR)
            self.saveFile(fpath, code)
            self.msg("dev", f"Save Nasm code: {fpath}", sender=self.name)
        return raw_object
    
    def _build_cpp_raw_worm(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Build CPP Raw Worm"
        raw_code = self.Coder.buildCppCode(raw_object.modules, raw_object.fpath_dir_output, raw_object.FILE_NAME)
        for fpath, rcode in raw_code.items():
            code = self.renderSingleTemplate(rcode, raw_object.VAR)
            self.saveFile(fpath, code)
            self.msg("dev", f"Save Cpp code: {fpath}", sender=self.name)
        return raw_object
    
    def _build_unknown_raw_worm(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Build Unknown Raw Worm"
        self.saveFile(raw_object.fpath_src_file, raw_object.master_module.raw_code)
        # raw_object.source_files[raw_object.fpath_src_file] = raw_object.master_module.raw_code
        return raw_object
    
    def _build_python_raw_worm(self, raw_exe: RawExe) -> RawExe:
        raw_exe.last_process_name = "Build Python Raw Worm"
        py_data = self.Coder.buildPythonCode(raw_exe.modules, raw_exe.fpath_dir_output, raw_exe.FILE_NAME)
        # UPDATE VARIABLES
        # update pip module for loader if use
        raw_exe.VAR["_PY_PIP_IMPORT"].extend(py_data["pip_import"])
        raw_exe.VAR["_PY_IMPORT"].extend(py_data["py_import"])
        
        code = self.renderSingleTemplate(py_data["raw_code"], raw_exe.VAR)
        self.saveFile(py_data["fpath"], code)

        return raw_exe
    
    def process_BuildCode(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = f"Build Code: {raw_object.NAME}"
        if raw_object.hiveType == "payload":
            self.process_BuildPayloadCode(raw_object)
            return raw_object
        match raw_object.code_lang:
            case "nasm":
                raw_object = self._build_nasm_raw_worm(raw_object)
            case "cpp":
                raw_object = self._build_cpp_raw_worm(raw_object)
            case "c++":
                raw_object = self._build_cpp_raw_worm(raw_object)
            case "python":
                self._build_python_raw_worm(raw_object)
            case _:
                raw_object = self._build_unknown_raw_worm(raw_object)
        return raw_object
    
    def process_BuildPayloadCode(self, raw_exe: RawExe) -> RawExe:
        raw_exe.last_process_name = "Process Build Payload Code"
        code = self.renderSingleTemplate(raw_exe.processCode, raw_exe.VAR)
        raw_exe.updateProcessCode(code)
        return raw_exe

    #############################################################################################################

    def process_BuildStaticLib(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Process Build Static Library"
        self.msg("msg", "Building static library....", sender=self.name)
        for lib in raw_object.master_raw.worm_list_LIB:
            lib = self._buildStaticLib(lib)
        return raw_object
    
    def _buildStaticLib(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Build Static Library"
        self.msg("msg", f"Build Static Library: {raw_object.FILE_NAME}", sender=self.name)
        self.executeProcessList(raw_object, raw_object.module_process)
        return raw_object
    

    ###################################################################################################

    ######################################## PAYLOADS #################################################

    def _build_payload_parent(self, raw_exe: RawExe, process_list: list) -> RawExe:
        proc_list = self.prepareProcess(process_list)
        self.executeProcessList(raw_exe, proc_list)
        return raw_exe

    def _build_payload(self, raw_exe: RawExe) -> RawExe:
        self.msg("msg", f"Building PAYLOAD: '{raw_exe.NAME}'....", sender=self.name)
        if len(raw_exe.module_process) == 0:
            raw_exe.updateProcessCode(raw_exe.master_module.raw_code)
        else:
            # check payload process
            self.executeProcessList(raw_exe, raw_exe.module_process)

        # check parent module process
        parent_proc = raw_exe.master_module.owner.payloadProcess.get(raw_exe.NAME)
        if parent_proc:
            self._build_payload_parent(raw_exe, parent_proc)
        # update Variables
        raw_exe.VAR[raw_exe.NAME] = raw_exe.processCode
        return raw_exe

    def process_BuildPayload(self, raw_exe: RawExe) -> RawExe:
        raw_exe.last_process_name = "Process Build Payload"
        self.msg("msg", "Check for payloads...", sender=self.name)
        for pay in raw_exe.master_raw.worm_list_PAYLOAD:
            self._build_payload(pay)
        return raw_exe

    ####################################################################################################

    ##################### COMPILE ##############################################

    def process_Compile(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Process Compile"
        comp = RawCompiler(raw_object, raw_object.compilerItem)
        raw_object.raw_compiler = comp
        # dual-base rendering
        cvar = ChainMap(raw_object.VAR, comp.conf)
        code = self.renderSingleTemplate(comp.raw_code, cvar)
        check = comp.updateConfig(code)
        if not check:
            self.msg("error", raw_object.last_process_error, sender=self.name)
            return raw_object
        self.masterCompiler.startCompile(raw_object)


      
        return raw_object
    

    ###################################################################################

    def process_FinalStep(self, raw_object: RawExe) -> RawExe:
        raw_object.last_process_name = "Process Final Step"
        # copying file
        self.msg("msg", "Copying necessary files for the worm to run...", sender=self.name)
        master = raw_object.master_raw
        tpath = master.dir_ready_app
        for name, fpath in master.addReadyApp.items():
            self.msg("msg", f"Copying file: {name}", sender=self.name)
            try:
                shutil.copy2(fpath, os.path.join(tpath, name))
            except Exception as e:
                self.msg("error", f"[!!] ERROR Copying file: '{name}' : {e} [!!]", sender=self.name)
        self.msg("msg", f"DONE ! Worm and all files necessary for its operation are located in the directory: {tpath}", sender=self.name)
        return raw_object
    
    #####################################################################################

    def _shadow_code(self, raw_exe: RawExe, shadow_mod: object) -> RawExe:
        self.msg("msg", f"Process Shadow: {shadow_mod.name}....")
        sh_mod = self.SpecialModules.getModule("shadow", shadow_mod.name)
        if not sh_mod:
            return raw_exe
        code = self.loadCode(raw_exe.fpath_src_file)
        
        code = shadow_mod.raw_code + "\n" + code
        if not code:
            return raw_exe
        code = sh_mod.PROCESS(code, raw_exe.VAR)
        # merge code
        if shadow_mod.shadowRender:
            sh_code = self.renderSingleTemplate(shadow_mod.raw_code, raw_exe.VAR)
            shadow_mod.addCode(sh_code)
        code = shadow_mod.raw_code + "\n" + code
        self.saveFile(raw_exe.fpath_src_file, code)
        self.msg("msg", f"Process Shadow: {shadow_mod.name} done.", sender=self.name)
        return raw_exe

    def process_ShadowCode(self, raw_exe: RawExe) -> RawExe:
        raw_exe.last_process_name = "Process Shadow Code"
        self.msg("msg", "Check for shadows...", sender=self.name)
        for mod in raw_exe.modules:
            if mod.itemType == "shadow":
                self._shadow_code(raw_exe, mod)
        
        return raw_exe



    

    
    # def _build_compiler_conf(self, raw_object: RawExe) -> dict:
    #     conf = {}
    #     code = self.renderSingleTemplate(raw_object.compilerItem.raw_code)
    #     try:
    #         code = json.loads(code)
    #     except json.JSONDecodeError as e:
    #         self.msg("error", f"[!!] ERROR: JSON decode compiler configuration: {e} [!!]", sender=self.name)
    #         raw_object.last_error = 1
    #         return conf
    #     return conf




