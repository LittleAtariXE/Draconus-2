import sys
import os
import multiprocessing
import threading

from time import sleep



from .tools.builder import Builder
from .tools.messanger_server import MessangerServer
from .tools.draco_task import Tasker
from .tools.draco_controler import DracoController
from .central.central import Central



class Draconus:
    def __init__(self, builder_object: Builder):
        self.CONF = builder_object

        self.fpath_draconus_lock = os.path.join(self.CONF.DIR_SYS_FILES, self.CONF.DRACONUS_LOCK_FILE_NAME)

        self.EXIT_PAUSE_CLEAN = 2
        self.FLAG_working = False

        self._sys_files = [
            self.fpath_draconus_lock,
            self.CONF.FD_SOCKET_DRACO_MSG,
            self.CONF.FD_SOCKET_DRACO_CONTROLER
        ]

    
    def build(self) -> bool:
        self.FLAG_working = True
        self.msg = MessangerServer(self.CONF, "Draconus")
        self.msg.Start()
        self.Tasker = Tasker(self, self.CONF)
        self.Tasker.Start()
        # add messanger to Tasker
        self.Tasker.addWorkingThread("Messanger", self.msg.messanger_th, "Responsible for sending messages to Commander.")
        # build Controller
        self.Ctrl = DracoController(self)
        if not self.Ctrl.build():
            return False
        self.Ctrl.Start()
        self.Central = Central(self, self.CONF)
        self.Central.Start()


        return True
    
    def _check_lock_file(self) -> bool:
        if os.path.exists(self.fpath_draconus_lock):
            return True
        else:
            return False
    
    def _build_system(self) -> bool:
        # checking if Draconus is already running
        if self._check_lock_file():
            print("[!!] ERROR: Draconus propably is running. [!!]")
            return False
        # make lock file
        try:
            with open(self.fpath_draconus_lock, "w") as file:
                file.write("lock")
        except Exception as e:
            print(f"[!!] ERROR making lock file: {e} [!!]")
            return False
        
        return True
    
    def _clean_system(self) -> None:
        for sf in self._sys_files:
            try:
                os.remove(sf)
            except:
                pass
    
    def _draco_start(self) -> None:
        if not self._build_system():
            return
        if not self.build():
            return
        c = 0
        while self.FLAG_working:
            sleep(0.5)
        self.funcExit()


    def Start(self) -> None:
        self._draco_start()
    
    def funcExit(self) -> None:
        self.msg("msg", "Closing Draconus....")
        self.Central.close_central()
        self.FLAG_working = False
        sleep(self.EXIT_PAUSE_CLEAN)
        self._clean_system()
        print("EXIT PROGRAM")

    
    def Exit(self) -> None:
        self._clean_system()
        print("EXIT")
    
    ##################### SYSTEM COMMAND ###################################
    def execute_sys_cmd(self, cmd: dict) -> None:
        main = cmd.get("cmd")
        if not main:
            self.msg("error", "[!!] ERROR: no command. [!!]")
            return
        match main:
            case "quit":
                self.FLAG_working = False
            case "task_show":
                self.Tasker.showTasks()
            case "build_server":
                self.Central.build_server(cmd.get("server_data", {}))
            case "close":
                self.Central.close_server(cmd.get("server_name", ""))
            case "client_conn":
                self.Central.send_client_to_commander(cmd.get("client_id"))
            case "client_msg":
                self.Central.sendMsgToClient(cmd.get("client_id"), cmd.get("msg", ""))
            case "client_show":
                self.Central.showClients()
            case "server_show":
                self.Central.showServers()
            case _:
                self.msg("error", f"[!!] ERROR: Unknown command: '{main}'. [!!]")
    

    ###############################################################################

