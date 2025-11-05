from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional
from .raw_exe import RawExe

if TYPE_CHECKING:
    from app.hive.worm_construtor import WormConstructor
    from app.hive.Lib.src.items_src.raw_lib_item import RawLibItem


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
        ### default DLL list for linker
        self.DEFAULT_LINKER_DLL_LIST = self.WC.queen.conf.DEFAULT_LINKER_DLL
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
        self.worm_list_DLL = self.worm_split["dll"]
        self.worm_list_MASTER = self.worm_split["master"]
        self.worm_list_PAYLOAD = self.worm_split["payload"]

        self.worm_MASTER = self.worm_list_MASTER[-1]

        # Worm Icon
        self.worm_icon = self.RWB.Icons.icon
        self.worm_icon_fpath = self.RWB.Icons.icon_fpath

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



    ################################# SPLIT WORM ######################################################


    def _set_master_worm_type(self, module: RawLibItem) -> str:
        if not module.fileType:
            return "exe"
        elif module.fileType == "dll":
            return "dll"
        elif module.fileType == "lib":
            return "lib"
        else:
            return "exe"
        
    def _makeSplitWorm(self, modules_list: list) -> dict:
        worm = {}
        worm["lib"] = []
        worm["dll"] = []
        worm["master"] = []
        worm["payload"] = []
        mod_used = []
        for mod in modules_list:
            if mod.itemType == "worm":
                output_ftype = self._set_master_worm_type(mod)
                raw = RawExe(self.WC, self, mod, "worm", output_ftype)
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
        worm["dll"] = self._prepareDynamicLib(raw_split["dll"])
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
    
    def _prepareDynamicLib(self, raw_exe_list: list) -> list:
        return self._prepareStaticLib(raw_exe_list)
    
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
        
