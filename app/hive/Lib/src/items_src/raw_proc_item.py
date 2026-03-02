from .raw_lib_item import RawLibItem


class RawProcessItem(RawLibItem):
    def __init__(self, raw_info_item: object):
        super().__init__(raw_info_item)

        self.process_sheme = self.load_sheme()
    
    def load_sheme(self) -> list:
        sheme = []
        try:
            with open(self.fpath, "r") as file:
                data = file.read()
        except:
            return sheme
        
        for line in data.split("\n"):
            if line.startswith(self.separator):
                continue
            if line == "" or line == "\n":
                continue
            sheme.append(line.strip("[]"))
        return sheme