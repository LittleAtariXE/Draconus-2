
import threading
from typing import Union
from time import sleep

from .servers.raw_server import RawTcpServer
from .servers.b64_server import B64TcpServer
from .servers.deliver_server import DeliverTcpServer
from .servers.raw_down import RawDown



class ClientHandler:
    def __init__(self, client_id: int, conn_obj: object, addr_obj: object, server: object, central: object):
        self.ID = client_id
        self.conn = conn_obj
        self.addr = addr_obj
        self.server = server
        self.owner = self.server.server_name
        self.central = central
        self.name = f"<{self.ID}>{self.addr[0]}:{self.addr[1]}"
        self._FLAG_conn = True

        self.RECIVE_TIMEOUT = self.central.CONF.tcp_sock_to_recive
        self.conn.settimeout(self.RECIVE_TIMEOUT)

        
    @property
    def FIRST_JOB(self) -> str:
        return self.server.FIRST_JOB
    
    @property
    def FLAG_connection(self) -> bool:
        if not self.server.FLAG_server_working.is_set():
            return False
        return self._FLAG_conn
    
    @property
    def FLAG_working(self) -> bool:
        if self.server.FLAG_server_working.is_set():
            return True
        else:
            return False
    
    def send_message(self, data: any) -> None:
        self.server.send_data(self, data)
    
    def start_recive(self) -> None:
        self.server.recive_data(self)
    
    
    def _close(self) -> None:
        self._FLAG_conn = False
        try:
            self.conn.close()
        except:
            pass
        self.central.msg("msg", f"Close connection: {self.name}", sender=self.server.draco_name)
    
    def close(self) -> None:
        self._FLAG_conn = False




class Central:
    def __init__(self, draconus: object, builder_object: object):
        self.Draconus = draconus
        self.Tasker = self.Draconus.Tasker
        self.msg = self.Draconus.msg
        self.CONF = builder_object

        self.client_ID = 0
        self.clients = {}
        self.servers = {}
        self.lock_client_id = threading.Lock()
        self.lock_clients = threading.Lock()

        self.CLOSE_CENTRAL_PAUSE = self.CONF.tcp_sock_to_listening
        self.CLEANER_PAUSE = self.CONF.central_clean_pause
        self.CONSOLE_SCR = self.CONF.console_screen

    def _get_server_type(self, type_name: str) -> Union[object, None]:
        match type_name.lower():
            case "raw":
                return RawTcpServer
            case "b64":
                return B64TcpServer
            case "deliver":
                return DeliverTcpServer
            case "rdown":
                return RawDown
            case _:
                return None
    
    
        

    def _build_server(self, data_conf: dict) -> Union[object, None]:
        serv_name = data_conf.get("name")
        if not serv_name:
            self.msg("error", "[!!] ERROR: Missing config: 'name' [!!]")
            return None
        serv_port = data_conf.get("port")
        try:
            serv_port = int(serv_port)
        except ValueError as e:
            self.msg("error", f"[!!] ERROR: Wrong port number: '{serv_port}'. [!!]")
            return None
        serv_type = data_conf.get("serv_type", "Raw")
        serv_type = self._get_server_type(serv_type)
        if not serv_type:
            self.msg("error", "[!!] ERROR: Unknown server type. [!!]")
            return None
        serv_ip = data_conf.get("ip", self.CONF.ip)
        #### extra config
        ex_conf = {}
        if data_conf.get("socket_encode"):
            ex_conf["TCP_SOCKET_FORMAT"] = data_conf.get("socket_encode")
        try:
            server = serv_type(self, serv_name, serv_port, serv_ip, config=ex_conf)
        except Exception as e:
            self.msg("error", f"[!!] ERROR Building server: {e} [!!]")
            return None
        
        return server

    
    def build_server(self, data_conf: dict) -> bool:
        server = self._build_server(data_conf)
        if not server:
            return False
        self.servers[server.server_name] = server
        server.start()
        self.Tasker.addWorkingThread(name=server.server_name, thread=server, info=f"Server-{server.server_name} on port: {server.server_port} Main Thread", th_type="server")
        return True
    
    ##################### ADD NEW CONNECTIONS #######################################

    def _ac_recive(self, client_handle: ClientHandler) -> None:
        self.Tasker.addThread(
            name = f"ClientHandle-{client_handle.ID}",
            func_name = client_handle.start_recive,
            info = f"Receiving data by client ID {client_handle.ID} on server: {client_handle.server.server_name}.",
            th_type = "Handle",
            daemon = False,
            start_now = True
        )
    
    def _ac_raw_send(self, client_handle: ClientHandler) -> None:
        self.Tasker.addThread(
            name = f"ClientHandle-{client_handle.ID}",
            func_name = client_handle.server.send_raw_data,
            fargs = (client_handle, ),
            info = f"Sending file to client ID: {client_handle.ID} on server: {client_handle.server.server_name}.",
            th_type = "Handle",
            daemon = True,
            start_now = True
        )

    def add_new_connection(self, conn_obj: object, addr_obj: object, server: object) -> None:
        with self.lock_client_id:
            cli_id = self.client_ID
            self.client_ID += 1
        new = ClientHandler(cli_id, conn_obj, addr_obj, server, self)
        with self.lock_clients:
            self.clients[str(new.ID)] = new
        self.msg("msg", f"New connection: {new.addr[0]}:{new.addr[1]}", sender=server.draco_name)

        match new.FIRST_JOB:
            case "recive":
                self._ac_recive(new)
            case "raw_send":
                self._ac_raw_send(new)
            case _:
                self.msg("error", f"[!!] ERROR: Unknown '{new.server.server_name}' function to work. Set to 'recive'.[!!]")
                self._ac_recive(new)
        
    
    #######################################################################################

    def close_server(self, server_name: str) -> None:
        server = self.servers.get(server_name)
        if not server:
            self.msg("error", f"[!!] ERROR: Server '{server_name}' does not exists. [!!]")
            return
        self.msg("msg", f"Close server: {server_name}...")
        for c in self.clients.values():
            if c.owner == server.server_name:
                c.close()
        server.close_server()

    def close_central(self) -> None:
        self.msg("msg", "Closing Central...")
        for cli in self.clients.values():
            cli.close()
        for serv in self.servers.values():
            serv.close_server()
        sleep(self.CLOSE_CENTRAL_PAUSE)
        self.msg("msg", "Central is closed.")
    
    def central_cleaner(self) -> None:
        while self.Draconus.FLAG_working:
            too_clean = []
            with self.lock_clients:
                for cli in self.clients.values():
                    if not cli._FLAG_conn:
                        too_clean.append(str(cli.ID))
                for tc in too_clean:
                    del self.clients[tc]
            sleep(self.CLEANER_PAUSE)
    
    def send_client_to_commander(self, client_id: Union[str, int]) -> None:
        client_id = str(client_id)
        client = self.clients.get(client_id)
        if not client:
            self.msg("error", f"ERROR: Client with ID {client_id} is not connected")
            self.Draconus.Ctrl.send_data({})
            return
        data = {
            "client_id" : client.ID,
            "server_name" : client.owner,
            "client_name" : client.name,
        }
        self.Draconus.Ctrl.send_data(data)
    
    def sendMsgToClient(self, handler_id: Union[int, str], data: any) -> None:
        handler = self.clients.get(str(handler_id))
        if not handler:
            self.msg("error", f"[!!] ERROR: Client Handler: '{handler_id}' is not connected. [!!]")
            return
        handler.send_message(data)
    
    def showClients(self) -> None:
        self.msg("msg", "  Connected Clients:  ", mtypes="title")
        if len(self.clients) == 0:
            return
        tab = {}
        tab["headers"] = ["Client ID", "IP:Port", "Server Name", "System"]
        tab["data"] = []
        for cli in self.clients.values():
            tab["data"].append([cli.ID, f"{cli.addr[0]}:{cli.addr[1]}", cli.owner, "Unknown"])
        tab["width"] = self.CONSOLE_SCR["4c"]
        
        self.msg("msg", tab, mtypes="table")
    
    def showServers(self) -> None:
        self.msg("msg", "  Active Servers:  ", mtypes="title")
        if len(self.servers) == 0:
            return
        # clients count
        cli_num = {}
        for s in self.servers.values():
            cli_num[s.server_name] = 0
        for c in self.clients.values():
            cli_num[c.owner] += 1
        tab = {}
        tab["headers"] = ["Server Name", "Server Type", "Connected Clients"]
        tab["data"] = []
        for s in self.servers.values():
            tab["data"].append([s.server_name, s.server_type, cli_num[s.server_name]])
        tab["width"] = self.CONSOLE_SCR["3c"]
        self.msg("msg", tab, mtypes="table", no_separator=True)
        

    

    def Start(self) -> None:
        self.Tasker.addThread(
            name = "CentralCleaner",
            func_name = self.central_cleaner,
            info = "Clears inactive connections.",
            daemon = True,
            start_now = True
        )
        self.msg("msg", "Central is ready.")
        


    def process_msg(self, msg: str, handler: ClientHandler, process_list: list = []) -> None:
        if len(process_list) == 0 or not process_list:
            self.msg("msg", msg, sender=handler.name)
        