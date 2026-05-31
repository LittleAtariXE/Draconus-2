import os
import socket

from threading import Thread, Event
from time import sleep



class TcpServer(Thread):
    def __init__(self, central: object, name: str, port: int, ip_addr: str = None, is_daemon: bool = True):
        super().__init__(daemon=is_daemon)
        self.central = central
        self.msg = self.central.msg
        self.CONF = self.central.CONF
        self.server_port = port
        if not ip_addr:
            self.server_ip = self.CONF.ip
        else:
            self.server_ip = ip_addr
        self.server_name = name
        self.draco_name = f"Server-{self.server_name}"
        
        ## A special designation that determines what first action the server will take after a connection from a client.
        ## E.g.: receiving messages, sending messages, etc.
        self.FIRST_JOB = "recive"


        self.FLAG_server_working = Event()
        self.FLAG_server_working.clear()
        self.SERVER_LISTENING_TIMEOUT = self.CONF.tcp_sock_to_listening
        self.DIR_INPUT_PATH = self.CONF.DIR_INPUT
    
    def build_server(self) -> bool:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
        except Exception as e:
            self.msg("error", f"[!!] ERROR building server: {e} [!!]")
            return False
        
        self.msg("msg", f"Server <{self.server_name}> on port: {self.server_port} build successfull.")
        return True
    

    def listening(self) -> None:
        if not self.FLAG_server_working.is_set():
            self.msg("error", "[!!] ERROR: Server can't listening. [!!]", sender=self.draco_name)
            return
        self.server_socket.settimeout(self.SERVER_LISTENING_TIMEOUT)
        try:
            self.server_socket.listen()
        except Exception as e:
            self.msg("error", f"[!!] ERROR Server listening: {e} [!!]", sender=self.draco_name)
        self.msg("msg", "Server start listening. Waiting for connections....", sender=self.draco_name)
        while self.FLAG_server_working.is_set():
            try:
                conn, addr = self.server_socket.accept()
                self.accept_connections(conn, addr)
            except TimeoutError:
                continue
            except Exception as e:
                self.msg("error", f"[!!] ERROR Accepting connection: {e} [!!]", sender=self.draco_name)
        
        self.msg("msg", "Server stop listening. Close connections....", sender=self.draco_name)
        self._close_server()
    
    def accept_connections(self, conn: object, addr: object) -> None:
        self.central.add_new_connection(conn, addr, self)

    def recive_file(self, handler: object, **kwargs) -> None:
        self.msg("error", "The server does not support file downloads.", sender=self.draco_name)
    
    def send_file(self, handler: object, fname: str, **kwargs) -> None:
        self.msg("error", "The server does not support file uploads.", sender=self.draco_name)
    
    def _close_server(self) -> None:
        # self.FLAG_server_working.clear()
        # sleep(self.SERVER_LISTENING_TIMEOUT)
        try:
            self.server_socket.close()
        except:
            pass
        self.msg("msg", "Server closed.", sender=self.draco_name)

    def close_server(self) -> None:
        self.FLAG_server_working.clear()

    def run(self) -> None:
        self.FLAG_server_working.set()
        if self.build_server():
            self.listening()
    