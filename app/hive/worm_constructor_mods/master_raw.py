from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional
from .raw_exe import RawExe

if TYPE_CHECKING:
    from app.hive.worm_construtor import WormConstructor


class MasterRaw:
    def __init__(self, worm_constructor: WormConstructor, worm_options: dict, variables: Optional[dict] = {}):
        self.WC = worm_constructor
        self.RWB = self.WC.RWB
        self.options = worm_options
        self.VAR = variables
        self.SEPARATE_MODULES_TYPE = ["lib", "dll"]

        self.allMods = self.RWB.wormAllMods

        self.worm_name = self.options.get("WORM_NAME")
        self.dir_output = self.options.get("DIR_OUTPUT")
        self.dir_ready_app = os.path.join(self.dir_output, f"{self.worm_name}{self.options['DIR_READY_SUFFIX']}")

        ### 
        self.DIR_HIVE_IN_DOCKER = self.WC.DIR_HIVE_IN_DOCKER_IMAGE
        self.DIR_READY_APP_IN_DOCKER = os.path.join(self.DIR_HIVE_IN_DOCKER, f'{self.worm_name}{self.options.get("DIR_READY_SUFFIX")}')
        ###

        # lib items
        self.main_compiler = None
        self.worm_process = self.RWB.RAW.wprocess
        self.worm_process_step = self.worm_process.process_sheme
        self.worm_process_execute = []
        self.worm_master = self.RWB.RAW.master_worm
        self.worm_master_compiler = self.RWB.RAW.master_compiler

        

        self._raw_worm_split = self._makeSplitWorm(self.allMods)
        self._worm_split = self.makeSplitWorm(self._raw_worm_split)
        self.worm_split = self.prepareWorm(self._worm_split)

        # RawExe
        self.worm_list_LIB = self.worm_split["lib"]
        self.worm_list_DLL = []
        self.worm_list_MASTER = self.worm_split["master"]
        self.worm_list_PAYLOAD = self.worm_split["payload"]

        self.worm_MASTER = self.worm_list_MASTER[-1]

        ### UPDATE ALL RAW_EXE
        self.updateRawExe()


    @property
    def allRawExe(self) -> list:
        rw = self.worm_list_MASTER
        rw.extend(self.worm_list_LIB)
        rw.extend(self.worm_list_DLL)
        return rw

    @property
    def addReadyApp(self) -> dict:
        ra = {}
        for rw in self.allRawExe:
            if rw.is_readyApp:
                ra[rw.final_output_name] = rw.final_output_fpath
        return ra

        
    def _makeSplitWorm(self, modules_list: list) -> dict:
        worm = {}
        worm["lib"] = []
        worm["dll"] = []
        worm["master"] = []
        worm["payload"] = []
        mod_used = []
        for mod in modules_list:
            if mod.itemType == "worm":
                raw = RawExe(self.WC, self, mod, "worm")
                worm["master"].append(raw)
                continue
            if mod.fileType:
                match mod.fileType.lower():
                    case "lib":
                        raw = RawExe(self.WC, self, mod, "lib", "lib")
                        worm["lib"].append(raw)
                    case "dll":
                        raw = RawExe(self.WC, self, mod, "dll", "dll")
                        worm["dll"].append(raw)

        # check for payload
        for pname, item in self.RWB.RAW._payloads.items():
            item.name = pname
            raw = RawExe(self.WC, self, item, "payload", "")
            worm["payload"].append(raw)


        return worm


    def makeSplitWorm(self, raw_split: dict) -> dict:
        for pay in raw_split["payload"]:
            pay = self._getChild(pay)
        for lib in raw_split["lib"]:
            lib = self._getChild(lib)
        for dll in raw_split["dll"]:
            dll = self._getChild(dll)
        for master in raw_split["master"]:
            master = self._getChild(master)
        return raw_split
    
    def prepareWorm(self, raw_split: dict) -> dict:
        worm = {}
        worm["lib"] = self._prepareStaticLib(raw_split["lib"])
        worm["master"] = self._prepareMasterWorm(raw_split["master"])
        worm["payload"] = self._preparePayloads(raw_split["payload"])
        return worm
    
    def _prepareStaticLib(self, raw_exe_list: list) -> list:
        last = []
        first = []
        for rex in raw_exe_list:
            if rex.master_module.owner == self.worm_master:
                last.append(rex)
            else:
                first.append(rex)
        
        first.extend(last)
        return first
    
    def _prepareMasterWorm(self, raw_exe_list: list) -> list:
        return raw_exe_list
    
    def _preparePayloads(self, raw_exe_list: list) -> list:
        return raw_exe_list

    
    def _getChild(self, raw_exe: RawExe) -> RawExe:
        child = self.RWB.wormGetChild(raw_exe.master_module)
        for cm in child:
            if cm.fileType:
                if cm.fileType.lower() in self.SEPARATE_MODULES_TYPE:
                    continue
            raw_exe.addRawModule(cm)
        return raw_exe
    
    ####### UPDATE FUNCTIONS ######################

    def updateRawExe(self) -> None:
        mods = self.allRawExe
        # add payload raw_exe
        mods.extend(self.worm_list_PAYLOAD)

        for mod in mods:
            mod.update()
        
    
 


# class MasterRaw:
#     def __init__(self, worm_constructor: WormConstructor, worm_options: dict, variables: Optional[dict] = {}):
#         self.WC = worm_constructor
#         self.RWB = self.WC.RWB
#         self.options = worm_options
#         self.VAR = variables

#         self.allMods = self.RWB.wormAllMods

#         self.worm_name = self.options.get("WORM_NAME")
#         self.dir_output = self.options.get("DIR_OUTPUT")
#         self.dir_ready_app = os.path.join(self.dir_output, f"{self.worm_name}{self.options['DIR_READY_SUFFIX']}")


#         self.main_compiler = None
#         self.worm_process = self.RWB.RAW.wprocess
#         self.worm_process_step = self.worm_process.process_sheme
#         self.worm_process_execute = []
#         self.worm_master = self.RWB.RAW.master_worm


#         self.worm_split = self.build_raw_template()
#         self.worm_raw_child = self.buildRawChild()
#         self.worm_raw_child_only = self.worm_raw_child[:-1]
#         self.worm_raw_child_master = self.worm_raw_child[-1]
#         self.WORM = []
    


#     def build_raw_template(self) -> dict:
#         # Splits the worm if individual modules require separate compilation.
#         _main = [self.worm_master]
#         _lib = []
#         _dll  = []
#         for mod in self.allMods:
#             if mod.fileType:
#                 match mod.fileType.lower():
#                     case "lib":
#                         _lib.append(mod)
#                     case "dll":
#                         _dll.append(mod)
        
#         sworm = {
#             "MAIN" : _main,
#             "DLL" : _dll,
#             "LIB" : _lib,
#         }

#         return sworm
    
#     def _buildRawLib(self, module: object) -> RawExe:
#         mod_list = [module]
#         child = self.RWB.wormGetChild(module)
#         # add support file
#         for mod in child:
#             if mod.itemType == "sfile":
#                 mod_list.append(mod)
#         raw_worm = RawExe(self.WC, self, mod_list, "lib", "lib")
#         return raw_worm
    
#     def _buildRawMaster(self, module: object) -> RawExe:
#         mod_list = [module]
#         child = self.RWB.wormGetChild(module)
#         # add support file
#         for mod in child:
#             if mod.itemType == "sfile":
#                 mod_list.append(mod)
#         raw_worm = RawExe(self.WC, self, mod_list, output_file_type="exe")
#         return raw_worm



#     def buildRawChild(self) -> list:
#         raw_worm_child = []
#         for mod in self.worm_split["LIB"]:
#             raw_lib = self._buildRawLib(mod)
#             raw_worm_child.append(raw_lib)
        
#         for master in self.worm_split["MAIN"]:
#             raw_exe = self._buildRawMaster(master)
#             raw_worm_child.append(raw_exe)
        
#         return raw_worm_child
    
    
        


        

        