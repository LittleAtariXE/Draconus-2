from typing import Union


class RawWorm:
    def __init__(self, raw_worm_builder: object):
        self.RWB = raw_worm_builder
        self.worm_name = "MyWorm"
        self.master_worm = None
        self.modules = {}
        self.sfiles = {}
        self.master_compiler = None
        self.mods_compiler = {}
        self._payloads = {}
        self.food = {}
        self.shadow = {}
        self.scode = None
        self.rscript = {}
        


    @property
    def allMods(self) -> list:
        if not self.master_worm:
            return []
        mods = [self.master_worm]
        for mod in self.modules.values():
            mods.append(mod)
        for sf in self.sfiles.values():
            mods.append(sf)
        if self.master_compiler:
            mods.append(self.master_compiler)
        for pay in self._payloads.values():
            mods.append(pay)
        for shadow in self.shadow.values():
            mods.append(shadow)
        if self.scode:
            mods.append(self.scode)
        # Add only master worm Resources script
        rscript = self.masterRcScript
        if rscript:
            mods.append(rscript)
        
        
        return mods
    
    @property
    def wprocess(self) -> Union[object, None]:
        if not self.master_worm:
            return None
        return self.master_worm.Wprocess
    
    @property
    def variables(self) -> dict:
        variables = {}
        for mod in self.allMods:
            for k, i in mod.Var.items():
                variables[k] = i
        return variables
    
    @property
    def payloads(self) -> dict:
        pay = {}
        for mod in self.allMods:
            for k, i in mod.payloadSpace.items():
                pay[k] = i
        return pay
    
    @property
    def masterRcScript(self) -> Union[object, None]:
        for rs in self.rscript.values():
            if rs.compilerOwner == self.master_compiler:
                return rs
        return None
    
    @property
    def tagsInfo(self) -> list:
        ti = self.master_worm.moduleTags
        if self.master_compiler:
            ti.extend(self.master_compiler.moduleTags)
        # if self.master_compiler.moduleTags:
        #     ti.extend(self.master_compiler.moduleTags)
        return ti
    
    @property
    def acceptItemList(self) -> list:
        if not self.master_worm:
            return []
        ail = set()
        for mod in self.allMods:
            ail.update(mod.typeAccept)
        return list(ail)
    
    def getModule(self, module_name: str) -> Union[object, None]:
        mod = None
        for m in self.allMods:
            if m.name == module_name:
                mod = m
                break
        return mod

    def getChild(self, owner_module: Union[str, object]) -> list:
        if isinstance(owner_module, str):
            owner_module = self.getModule(owner_module)
            if not owner_module:
                return []
        child = []
        for mod in self.allMods:
            if mod.owner == owner_module:
                child.append(mod)
        return child
    
    def getChildAll(self, owner_module: Union[str, object]) -> list:
        if isinstance(owner_module, str):
            owner_module = self.getModule(owner_module)
            if not owner_module:
                return []
        child = []
        for mod in self.allMods:
            if mod.owner == owner_module:
                child.append(mod)
                grand_child = self.getChild(mod)
                for m in grand_child:
                    if m in child:
                        continue
                    child.append(m)
        return child
    
    def checkFood(self, name: str) -> Union[object, str, None]:
        for mod in self.allMods:
            for food_name in mod.foodReq.values():
                if food_name == name:
                    return name
        for vn, var in self.variables.items():
            if vn == name:
                return var
        return None

    