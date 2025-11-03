import click
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
            self.pSort("msg [text]", 'Send message / command to client. Put message quotation marks “”')
            self.pSort("", 'Ex: msg "Hello World"')
        
        @cliShell.command()
        @click.argument("message")
        def msg(message):
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "client_msg"
            cmd["client_id"] = self.client_id
            cmd["msg"] = message
            self.cmd_SEND(cmd)
            

        return cliShell
    

    def Start(self) -> None:
        client_shell = self.shellBuild()
        client_shell()