
from termcolor import cprint


class SHELL_HELP_MESSAGES:
    def __init__(self, msg_sorter: object):
        self.msg_sorter = msg_sorter
        self.pSort = self.msg_sorter.sort_Text
        self.pTitle = self.msg_sorter.make_Title
        self.pText = self.msg_sorter.basic_Text
        

    
    @property
    def DRACONUS_SERVER_TYPE_HELP(self) -> None:
        self.pTitle("  Build server Help  ")
        self.pText("The server command creates a server, by default of type 'raw'. The created server is started and ready to accept connections.")
        self.pText("Servers are created by providing a name and a port on which it will listen. Optionally, an IP address can also be specified; by default it is taken from the main configuration.")
        self.pText("")
        self.pSort("name", "The server’s name, can be any string.")
        self.pSort("port", "The port on which the server listens (recommended range: 2000 – 64000).")
        self.pSort("--types, -t", "The type of server to create (default is 'raw').")
        self.pTitle("  Server Types:  ")
        self.pSort("raw", "A TCP socket server that sends and receives raw bytes, which are only converted to text.")
        self.pSort("", "It does not encode, encrypt, etc. It has a special buffer that merges fragments of messages into a whole.")
        self.pText("")
        self.pTitle("  Example:  ")
        self.pSort("server myServ 4444", "Building default 'raw' server on port 4444.")
        self.pSort("server new2 3000 -t b64", "Buiding 'b64' server on port 3000")
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
    def HIVE_COMP_VARIABLES_HELP(self) -> None:
        self.pTitle("  Compiler Variable help  ")
        self.pText("Compiler variables are values applied during the final build/compilation stage that control how the program is produced and how it will run.")
        self.pText("They define runtime settings (for example, whether the program runs in a console or as a background service),")
        self.pText("linking behavior, and other build-time options that affect the final executable.")
        self.pText("")
        self.pText("NO_STD_LIB - When enabled, the standard library is not linked into the executable.")
        self.pText("This usually produces a smaller binary but removes the standard library’s runtime support and utilities.")
        self.pText("Using NO_STD_LIB may require supplying your own startup/runtime code or replacements for any standard-library functions you use")
        self.pText("— some features that rely on the standard library may be unavailable.")
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
        self.pSort("--xlist, -xl", "Show the list of icons with additional information.")
        self.pText("")
        
    @property
    def HIVE_BUILD_COMPILE_HELP(self) -> None:
        self.pTitle("  Build help  ")
        self.pText("Compiles the worm. This is the final function that produces an executable (exe, dll, etc.) depending on what the chosen template supports.")
        self.pSort("--no_compile, -nc", "Do not compile the worm; only produce the generated source/code files. Warning: using this option may cause errors and some build steps may be skipped,")
        self.pSort("", "especially if the final worm requires additional libraries that will not be compiled. Code files will still be created.")
        self.pSort("--payload [name], -p [name]", "Do not compile the final binary; store the generated code in the payload library under the given name so it can be added to another worm later.")
        self.pSort("", "Example: you can assemble a worm from Python modules but save it as a payload to be used later (for example inside a shellcode).")
        self.pSort("--as_food [name], -as [name]", "Do not compile the final binary; store the generated code in the food library so it can be assigned to a variable and reused.")
        self.pSort("", "This is particularly useful for saving generated shellcodes that you want to add to other projects.")
        self.pText("")
        