import os
from typing import Union

from .src.items_src.raw_mod_info import RawModuleInfo
from .mods.shortcuts import Shortcuts


class Library:
    def __init__(self, queen: object):
        self.queen = queen
        self.msg = self.queen.msg
        self.CONSOLE_SCR = self.queen.conf.console_screen
        self.DEFAULT_TABLE_STYLE = "simple_grid"
        self.DIR_LIB_MAIN = self.queen.DIR_LIB_MAIN
        self.DIR_LIB_ICONS = os.path.join(self.DIR_LIB_MAIN, "icons")
        self.DIR_LIB_ITEMS = os.path.join(self.DIR_LIB_MAIN, "items")
        self.LIB_ITEM_SEPARATOR = "#!"
        self.DIR_LIB_ITEM_WORMS = os.path.join(self.DIR_LIB_ITEMS, "worms")
        self.DIR_LIB_ITEM_PROCESS = os.path.join(self.DIR_LIB_ITEMS, "process")
        self.DIR_LIB_ITEM_MODULES = os.path.join(self.DIR_LIB_ITEMS, "modules")
        self.DIR_LIB_ITEM_PAYLOADS = os.path.join(self.DIR_LIB_ITEMS, "payloads")
        self.DIR_LIB_ITEM_SFILES = os.path.join(self.DIR_LIB_ITEMS, "sfiles")
        self.DIR_LIB_ITEM_SUPPORT = os.path.join(self.DIR_LIB_ITEMS, "support")
        self.DIR_LIB_ITEM_FOOD = os.path.join(self.DIR_LIB_ITEMS, "food")
        self.DIR_LIB_ITEM_SHADOWS = os.path.join(self.DIR_LIB_ITEMS, "shadows")
        self.DIR_LIB_ITEMS_BINARY = os.path.join(self.DIR_LIB_ITEMS, "binary")
        self.DIR_LIB_ITEMS_CSCRIPT = os.path.join(self.DIR_LIB_ITEMS, "rscript")
        self.DIR_LIB_ITEMS_SHELLCODE_TEMPLATE = os.path.join(self.DIR_LIB_ITEMS, "scode_temp")
        self.DIR_LIB_ITEMS_COMPILERS = os.path.join(self.DIR_LIB_ITEMS, "compilers")
        self._load_counter = 0

        ## add shortucts
        self.shortcuts = Shortcuts(self.queen.conf, self)
        self.shortcuts.make_shortcuts()

        self.lib = {
            "worm" : {},
            "Wprocess" : {},
            "module" : {},
            "payload" : {},
            "sfile" : {},
            "support" : {},
            "food" : {},
            "shadow" : {},
            "scode" : {},
            "rscript" : {},
            "compiler" : {},
        }

    def load_items(self, dir_path: str, item_type: object = RawModuleInfo) -> None:
        # special options
        opt = {}
        # Passing path to binary files directory
        opt["BINARY_DIR"] = self.DIR_LIB_ITEMS_BINARY
        ###########
        for r,d,f in os.walk(dir_path):
            for fname in f:
                item = item_type(os.path.join(r, fname), opt, separator=self.LIB_ITEM_SEPARATOR)
                if item.FLAG_broken:
                    continue
                if not item.itemType in self.lib.keys():
                    self.msg("error", f"[!!] ERROR: Unknown item in library: {item.fpath} [!!]")
                else:
                    self.lib[item.itemType][item.name] = item
                    self._load_counter += 1
    
    def findItems(self) -> None:
        self.msg("msg", "Builiding library....")
        self._load_counter = 0
        self.load_items(self.DIR_LIB_ITEM_WORMS)
        self.load_items(self.DIR_LIB_ITEM_PROCESS)
        self.load_items(self.DIR_LIB_ITEM_MODULES)
        self.load_items(self.DIR_LIB_ITEM_SFILES)
        self.load_items(self.DIR_LIB_ITEM_SUPPORT)
        self.load_items(self.DIR_LIB_ITEM_PAYLOADS)
        self.load_items(self.DIR_LIB_ITEM_FOOD)
        self.load_items(self.DIR_LIB_ITEM_SHADOWS)
        self.load_items(self.DIR_LIB_ITEMS_SHELLCODE_TEMPLATE)
        self.load_items(self.DIR_LIB_ITEMS_CSCRIPT)
        self.load_items(self.DIR_LIB_ITEMS_COMPILERS)

        self.msg("msg", f"Scan complete. Found {self._load_counter} items.")
    
    def getLibItem(self, types: str, name: str, show_error: bool = True) -> Union[object, None]:
        mtype = self.lib.get(types)
        if not mtype:
            if show_error:
                self.msg("error", f"[!!] ERROR: Item type: '{types}' does not exist in library. [!!]")
            return None
        mitem = mtype.get(name)
        if not mitem:
            if show_error:
                self.msg("error", f"[!!] ERROR: Item: '{name}' does not exists in '{types}' library. [!!]")
            return None
        return mitem
    
    def showItem(self, item_type: str) -> None:
        items = self.lib.get(item_type)
        if not items:
            self.msg("error", f"[!!] ERROR: Items: '{item_type}' does not exists in library. [!!]")
            return
        tab = {}
        tab["headers"] = ["Name", "Tags", "Description"]
        tab["data"] = []
        for i in items.values():
            tags = ""
            for t in i.Tags:
                tags += f"[{t}] "
            tab["data"].append([i.Name, tags, i.Info])
        tab["width"] = self.CONSOLE_SCR["3c"]
        tab["types"] = self.DEFAULT_TABLE_STYLE
        self.msg("msg", f"  {item_type}  ", mtypes="title")
        self.msg("msg", tab, mtypes="table", no_separator=True)
    