
from termcolor import cprint


class SHELL_HELP_MESSAGES:
    def __init__(self, msg_sorter: object):
        self.msg_sorter = msg_sorter
        self.pSort = self.msg_sorter.sort_Text
        self.pTitle = self.msg_sorter.make_Title
        self.pText = self.msg_sorter.basic_Text
        self.pSort_set = self.msg_sorter.set_text_len_first
        self.pSort_restore = self.msg_sorter.restore_text_len_first
        

    
    @property
    def DRACONUS_SERVER_TYPE_HELP(self) -> None:
        self.pTitle("  Build server Help  ")
        self.pText("The server command creates a server, by default of type 'raw'. The created server is started and ready to accept connections.")
        self.pText("Servers are created by providing a name and a port on which it will listen. Optionally, an IP address can also be specified; by default it is taken from the main configuration.")
        self.pText("")
        self.pSort("name", "The server’s name, can be any string.")
        self.pSort("port", "The port on which the server listens (recommended range: 2000 – 64000).")
        self.pSort("--encode, -e", "Message encoding format. If not selected, the default will be used.")
        self.pSort("--types, -t", "The type of server to create (default is 'raw').")
        self.pTitle("  Server Types:  ")
        self.pSort("raw", "A TCP socket server that sends and receives raw bytes, which are only converted to text.")
        self.pSort("", "It does not encode, encrypt, etc. It has a special buffer that merges fragments of messages into a whole.")
        self.pText("")
        self.pSort("b64", "A regular TCP socket server encrypts and encodes communications using base64.")
        self.pText("")
        self.pSort("deliver", "A TCP socket server. After creating it, a directory with the server’s name will appear inside the 'INPUT' folder.")
        self.pSort("", "The server works by immediately sending the file located in that directory as soon as a client connects,")
        self.pSort("", "then closing the connection. It does not receive any messages.")
        self.pText("")
        self.pSort("rdown", "RawDown - A simple TCP socket server used for receiving files. It does not accept incoming messages,")
        self.pSort("", "but it can send messages through the socket. After creating the servera directory with the server’s name will appear inside the 'Loot' folder.")
        self.pSort("", "All received files will be stored there, each assigned a random filename.")
        self.pText("")
        self.pTitle("  Example:  ")
        self.pSort("server myServ 4444", "Building default 'raw' server on port 4444.")
        self.pSort("server new2 3000 -t b64", "Buiding 'b64' server on port 3000")
        self.pSort("server new10 5000 -t b64 -e cp1250", "Builiding 'b64' server on port 5000 with encoding 'cp1250'.")
        self.pText("")

    @property
    def HIVE_VARIABLES_HELP(self) -> None:
        self.pTitle("  Variable help  ")
        self.pText('**** Entering and changing variables. The scheme is: variable_name "value". Ex: PORT "4444" ****')
        self.pText('**** Enter values ​​in quotation marks "". This will avoid errors. ****')
        self.pText('**** If you want to set the type of a variable use the "-t" option. ****')
        self.pText("**** Option: '-f' assigning FOOD variables to regular variables: var -f <variable_name> <FOOD_name> ****")
        self.pText("**** ex: var -f data FOOD_UserAgent")
        self.pText("")
        self.pTitle("  options:  ")
        self.pSort("--type, -t", "Set variable type. Ex: str, int, list etc.")
        self.pSort("", 'Ex: var port_num "[100, 200, 400]" -t list')
        self.pSort("--food, -f", "Add food to variable. '-f [target_variable] [food_name]'")
        self.pSort("", 'Ex: var -f worm_text FOOD_default_text')
        self.pText("")
    

    @property
    def HIVE_ICON_HELP(self) -> None:
        self.pTitle("  Icon help  ")
        self.pText("Sets the icon for the final worm executable. Draconus includes several built-in icons that can be used.")
        self.pText("The 'links' directory contains a shortcut to the icons folder; you can add your own icons there and select them for the worm.")
        self.pText("")
        self.pTitle("  options:  ")
        self.pSort("--set_icon, -s", "Set the chosen icon for the exe file.")
        self.pSort("--list, -l", "Show the list of available icons.")
        self.pText("")
        
    @property
    def HIVE_BUILD_COMPILE_HELP(self) -> None:
        self.pTitle("  Build help  ")
        self.pText("Compiles the worm. This is the final function that produces an executable (exe, dll, etc.) depending on what the chosen template supports.")
        self.pText("")
        self.pSort("--no_compile, -nc", "Do not compile the worm; only produce the generated source/code files. Warning: using this option may cause errors and some build steps may be skipped,")
        self.pSort("", "especially if the final worm requires additional libraries that will not be compiled. Code files will still be created.")
        self.pSort("", "")
        self.pSort("--payload, -p", "Places the built worm into the 'payload' section of the library. If the worm has gone through compilation, its binary version will be saved.")     
        self.pSort("", "Using this option together with '--no_compile' will store only the worm's source/code in the 'payload' section (useful when building Python scripts).")
        self.pSort("", "Note: 'not compiled' payloads generally do not support multi-file projects, so this option will not work correctly for e.g. C++ code that requires multiple files.")
        self.pSort("", 'After the option you may provide a description in quotes (e.g. --payload "My description") which will be used as the modules description in the library.')
        self.pSort("", "Ex:")
        self.pSort("", 'build --no_compile --payload "My first python payload ...."')
        self.pSort("", 'build --payload "My Worm abc...."')
        self.pSort("", "")
        self.pSort("--shellpay, -sp", "Works only when generating shellcode. Saves the finished shellcode into the 'payload' section.")
        self.pSort("", 'After the option you may provide a description in quotes (e.g. --shellpay "My description") which will be used as the modules description in the library.')
        self.pSort("", "Ex:")
        self.pSort("", 'build --shellpay "My shellcode reverse tcp"')
        self.pSort("", "")
        self.pSort("--shellfood, -sf", "Works only when generating shellcode. Saves the finished shellcode into the 'food' section.")
        self.pSort("", 'After the option you may provide a description in quotes (e.g. --shellfood "My description") which will be used as the modules description in the library.')
        self.pSort("", "")
 
        self.pText("")
    
    @property
    def HIVE_MODULES_TYPE(self) -> None:
        self.pTitle("  DRACONUS Item type:  ")
        self.pSort_set(15)
        self.pSort("worm", "The main template; required to add first. Its choice determines whether you build an injector, shellcode, DLL, or something else.")
        self.pSort("", "Different extra modules can be attached to a worm depending on the chosen template.")
        self.pSort("", "")
        self.pSort("module", "Various modules or libraries that add functionality. Some worms allow additional modules to be added.")
        self.pSort("support", "Modules and libraries added automatically when required by a worm or another module.")
        self.pSort("payload", "Various kinds of payloads, small and large, implemented in different languages. If a worm supports adding payloads, they are listed here.")
        self.pSort("shadow", "Code obfuscation. Additional modules used to obfuscate code.")
        self.pSort("food", "'Food' for the worm. Contains assorted data like text databases for obfuscators, random game names, ready-made shellcodes, and other resources.")
        self.pSort("", "Worms automatically use food when needed, but you can change items or assign them to a variable 'var'.")
        self.pSort("", "")
        self.pSort("Wprocess", "The lifecycle a worm goes through to reach its final form. These are added automatically; only modify them if you really know what you are doing.")
        self.pSort("scode", "Template for creating shellcodes.")
        self.pSort("compiler", "Compilers and linker scripts that can be attached to a worm. Each worm has a default compiler assigned; you can change it if you know what you’re doing.")
        self.pSort("", "For example, you can switch a Python build from PyInstaller to Nuitka.")
        self.pSort("", "")
        self.pSort("rscript", "Additional .rc resource files that inject metadata or resources into the final executable.")
        self.pSort("", "These resource files can be added when the chosen compiler supports including .rc resources.")
        self.pSort("", "")
        print("\n")
        self.pSort_restore()
