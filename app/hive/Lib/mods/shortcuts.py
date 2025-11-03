import os


class Shortcuts:
    def __init__(self, builder: object, library: object):
        self.conf = builder
        self.library = library
        self.dir_shortcuts = self.conf.DIR_SHORTCUTS
    
        self.shortucts = {
            "icons" : self.library.DIR_LIB_ICONS
        }
    
    def make_shortcuts(self) -> None:
        for name, path in self.shortucts.items():
            link_path = os.path.join(self.dir_shortcuts, name)
            if os.path.exists(link_path):
                continue
            os.symlink(path, link_path)