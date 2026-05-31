import os



class Icons:
    def __init__(self, icon_dir: str):
        self.DIR_ICONS = icon_dir
        self.icon = None
        self.icon_fpath = None
    

    @property
    def icon_list(self) -> list:
        icon_list = []
        for fname in os.listdir(self.DIR_ICONS):
            icon_list.append(fname)
        return icon_list
    
    def set_icon(self, name: str) -> bool:
        if name in self.icon_list:
            self.icon = name
            self.icon_fpath = os.path.join(self.DIR_ICONS, name)
            return True
        else:
            return False
    
    def get_info(self) -> list:
        info = []
        for icon in self.icon_list:
            i_name = icon
            i_size = os.stat(os.path.join(self.DIR_ICONS, icon))
            i_size = i_size.st_size
            info.append((i_name, i_size))
        return info