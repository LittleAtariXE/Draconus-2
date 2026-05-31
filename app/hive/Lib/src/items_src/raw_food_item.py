from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .raw_lib_item import RawLibItem
if TYPE_CHECKING:
    from .raw_mod_info import RawModuleInfo




class RawFoodItem(RawLibItem):
    def __init__(self, raw_info_object: RawModuleInfo):
        super().__init__(raw_info_object)
        self.FOOD_SHOW_CHAR_LIMIT = 20

        # Defines how data will be loaded and placed
        self.loadType = None

        # Determines whether data will be rendered as for modules
        self.foodRender = False

        # OUTPUT FOOD DATA
        self.FOOD_DATA = None

        self.update_data()
        self.load_food()
    
    @property
    def showValue(self) -> str:
        return self.show_value
    
    @property
    def Value(self) -> any:
        return self.FOOD_DATA
    
    def update_data(self) -> None:
        for line in self.load_item_data():
            head = line.split(self.in_separator)
            match head[0]:
                case "loadType":
                    self.loadType = head[1]
                case "foodRender":
                    if head[0] == "True" or head[0] == True:
                        self.foodRender = True
                    else:
                        self.foodRender = False
    
    def show_value(self) -> str:
        fdata = str(self.FOOD_DATA)
        if len(fdata) > self.FOOD_SHOW_CHAR_LIMIT:
            fdata = fdata[0:self.FOOD_SHOW_CHAR_LIMIT]
            fdata += "..."
        return fdata

    def load_food_list(self) -> list:
        try:
            with open(self.fpath, "r") as file:
                rdata = file.read()
        except:
            return []
        data = []
        for line in rdata.split("\n"):
            if line.startswith(self.separator) or line == "\n" or line == "":
                continue
            data.append(line)
        return data
    
    def load_food(self) -> None:
        match self.loadType:
            case "list":
                self.FOOD_DATA = self.load_food_list()
            case "clean_text":
                self.FOOD_DATA = self.load_clean_text(self.load_food_list())
            case "text":
                self.FOOD_DATA = self.load_text(self.load_food_list())
            case _:
                self.FOOD_DATA = self.load_food_list()
    
    def load_clean_text(self, data: list) -> str:
        text = "".join(data)
        text = text.replace("\n", "")
        return text
    
    def load_text(self, data: list) -> str:
        return "\n".join(data)
    
    