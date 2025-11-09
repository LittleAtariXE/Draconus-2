
class RawModuleInfo:
    def __init__(self, fpath: str, options: dict = {}, separator="#!"):
        self.separator = separator
        self.in_separator = "##"
        self.fpath = fpath
        self._opt = options

       # Item name. 'name'
        self.name = None

        # Item description. #   'info'
        self.info = ""

        # Item Library types. # 'itemType'
        self.itemType = None

        # A special type for handling binary files. #   'binType' 
        # binType##True
        self.binType = False

        # Item tags. #  'itemTags'
        # WIN - Works only on Windows
        # LIN - Works only on Linux
        # LW - Works on Linux and Windows
        # PyS - Python standard script (standard library)
        # PyEx - Python script with external library
        # SM - Support Module
        self.itemTags = []

        # HIVE section module type. #   'hiveType'
        # PySM - Python module with std library
        # PyExM - Python module with external library
        # LIB - Static library
        # DLL - DLL library
        #   hiveType##name1##name2##name3 ... etc
        self.hiveType = []

        # acceptable HIVE modules. #    'typeAccept'
        # PySM - Python module with std library
        # PyExM - Python module with external library
        # LIB - Static library
        # DLL - DLL library
        #   typeAccept##name1##name2##name3 .... etc
        self.typeAccept = []

        # Module type from the system's point of view. #    'fileType'
        # DLL, LIB etc.
        #   fileType##DLL
        self.fileType = None

        # Item is broken. Dont add to library. #    "FLAG_broken"
        self.FLAG_broken = False

        # Item source code language
        # Python, Nasm, cpp, c, None
        #   lang##Python
        self.lang = None

        self._load_basic_data()

        

    
    def fGetBool(self, value: str) -> bool:
        if value == "True" or value == "true" or value == True:
            return True
        else:
            return False
    
    def _load_basic_data(self) -> None:
        data = []
        try:
            with open(self.fpath, "r") as file:
                for line in file.readlines():
                    if line.startswith(self.separator):
                        data.append(line.lstrip(self.separator).rstrip("\n"))   
        except Exception as e:
            return
        
        for hd in data:
            head = hd.split(self.in_separator)
            match head[0]:
                case "name":
                    self.name = head[1]
                case "info":
                    self.info += head[1]
                case "itemType":
                    self.itemType = head[1]
                case "hiveType":
                    self.hiveType.extend(head[1:])
                case "typeAccept":
                    self.typeAccept.extend(head[1:])
                case "fileType":
                    self.fileType = head[1]
                case "FLAG_broken":
                    self.FLAG_broken = self.fGetBool(head[1])
                case "lang":
                    self.lang = head[1]
                case "binType":
                    self.binType = self.fGetBool(head[1])

