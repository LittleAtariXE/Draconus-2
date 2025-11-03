
from typing import Union

from .items_src.raw_lib_item import RawLibItem
from .items_src.raw_proc_item import RawProcessItem
from .items_src.raw_compiler_item import RawCompilerItem
from .items_src.raw_food_item import RawFoodItem
from .worm_variable import WormVariable
from .default_variable import DefaultWormVariable
from .payload_variable import PayloadVariable

class RawItemConstructor:
    def __init__(self, queen: object):
        self.name = "RawItemConstructor"
        self.queen = queen
        self.msg = self.queen.msg
        self.defualt_variables = DefaultWormVariable(self.queen.conf)
        self.DEFAULT_VAR = self.defualt_variables.variables

    def fGetBool(self, value: str) -> bool:
        if value == "True" or value == "true" or value == True:
            return True
        else:
            return False
    
    def buildRawItem(self, raw_mod_info: object) -> Union[object, None]:
        match raw_mod_info.itemType:
            case "Wprocess":
                new = self.process_item(raw_mod_info, RawProcessItem)
            case "compiler":
                new = self.process_item(raw_mod_info, RawCompilerItem)
            case "food":
                new = self.process_item(raw_mod_info, RawFoodItem)
            case _:
                new = self.process_item(raw_mod_info, RawLibItem)
        
        return new
        
    
    def process_item(self, raw_mod_info: object, template_object: object) -> object:
        raw_mod = template_object(raw_mod_info)
        for head_line in raw_mod.load_item_data():
            head = head_line.split(raw_mod.in_separator)
            match head[0]:
                case "name":
                    raw_mod.name = head[1]
                case "info":
                    raw_mod.info += head[1]
                case "itemType":
                    raw_mod.itemType = head[1]
                case "hiveType":
                    raw_mod.hiveType.extend(head[1:])
                case "typeAccept":
                    raw_mod.typeAccept.extend(head[1:])
                case "fileType":
                    raw_mod.fileType = head[1]
                case "FLAG_broken":
                    raw_mod.FLAG_broken = self.fGetBool(head[1])
                case "lang":
                    raw_mod.lang = head[1]
                case "Wprocess":
                    raw_mod.Wprocess = head[1]
                case "readyApp":
                    raw_mod.readyApp = self.fGetBool(head[1])
                case "Var":
                    self.add_worm_variable(raw_mod, head[1:])
                case "foodAdd":
                    raw_mod.foodReq[head[1]] = head[2]
                case "reqMod":
                    raw_mod.reqMod.extend(head[1:])
                case "itemTags":
                    raw_mod.itemTags.extend(head[1:])
                case "modCompiler":
                    raw_mod.modCompiler = head[1]
                case "modProcess":
                    raw_mod.modProcess.extend(head[1:])
                case "inFile":
                    raw_mod.inFile[head[1]] = head[2]
                case "addNameComp":
                    raw_mod.addNameComp = self.fGetBool(head[1])
                case "addExeComp":
                    raw_mod.addExeComp = self.fGetBool(head[1])
                case "modName":
                    raw_mod.modName = head[1]
                case "compilerCore":
                    raw_mod.compilerCore = head[1]
                case "wormCompiler":
                    raw_mod.wormCompiler = head[1]
                case "compilerMCNAME":
                    raw_mod.compilerMCNAME = head[1]
                case "payloadSpace":
                    self.add_payload_variable(raw_mod, head[1:])
                case "payloadProcess":
                    raw_mod.payloadProcess[head[1]] = head[2:]
                case "pyType":
                    raw_mod.payType = head[1]
                case "pyImportHold":
                    raw_mod.payImportHold = self.fGetBool(head[1])
                case "shadowRender":
                    raw_mod.shadowRender = self.fGetBool(head[1])
        
        return raw_mod
    


    def add_worm_variable(self, raw_mod: object, head: list) -> None:
        vname = head[0]
        vvalue = head[1]
        vinfo = head[2]
        if len(head) > 3:
            vtype = head[3]
        else:
            vtype = "str"
        
        # check value
        # default variable
        if vvalue.startswith("$"):
            vvalue = self.DEFAULT_VAR.get(vvalue[1:])

        # NULL var
        if vvalue == "_NULL":
            var = WormVariable(vname, vinfo, raw_mod)
        else:
            var = WormVariable(vname, vinfo, raw_mod, vvalue, vtype)

        raw_mod.Var[vname] = var
    
    def add_payload_variable(self, raw_mod: object, head: list) -> None:
        pv = PayloadVariable(head[0], head[1], raw_mod)
        raw_mod.payloadSpace[head[0]] = pv
