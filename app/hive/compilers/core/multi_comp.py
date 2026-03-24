from __future__ import annotations
import docker
import os
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..master_compiler import MasterCompiler

class CrossCompCore:
    CORE_NAME = "CrossComp"
    def __init__(self, master_compiler: MasterCompiler):
        self.name = "CrossComp"
        self.master = master_compiler
        self.msg = self.master.msg
        self.docker = docker.from_env()
        self.container_id = None

        # Hive output dir
        self.HIVE_OUTPUT_DIR = self.master.DIR_HIVE_OUT
        # dokcer hive directory
        self.DOCKER_DIR_HIVE = self.master.DIR_HIVE_IN_DOCKER
        ##### docker image
        # self.DOCKER_IMAGE = "littleatarixe/wine_py:1.0"
        ##### new docker image
        self.DOCKER_IMAGE = "littleatari/cross_comp:1.0"
        # docker container name
        self.DOCKER_CONTAINER_NAME = self.master.COMPILER_CONTAINER_NAME
        # default DLL
        self.DEFAULT_DLL = "-lkernel32 -lmsvcrt -luser32 -lshell32 -lws2_32 -lshlwapi"
        self.STATIC_LINK = "-static-libstdc++ -static-libgcc"
    

    @property
    def compiler(self) -> Union[object, None]:
        return self.get_compiler()
    
    @property
    def status(self) -> bool:
        if self.get_compiler():
            return True
        else:
            return False

    def check_docker_image(self) -> bool:
        try:
            container = self.docker.images.get(self.DOCKER_IMAGE)
            return True
        except docker.errors.ImageNotFound:
            return False
    
    def get_compiler(self) -> Union[object, None]:
        if not self.check_docker_image():
            self.msg("error", "The compiler is incomplete. There is no Docker image installed..", sender=self.name)
            return None
        if self.container_id:
            return self.docker.containers.get(self.container_id)
        for con in self.docker.containers.list(all=True):
            if con.name == self.DOCKER_CONTAINER_NAME:
                self.container_id = con.id
                return self.docker.containers.get(self.container_id)
        
        return None
    
    # Execute Command in docker conatiner
    def eCMD(self, command: str, no_output: bool = False) -> None:
        exec_id = self.docker.api.exec_create(self.compiler.id, f"bash -c '{command}'")
        output = self.docker.api.exec_start(exec_id, stream=True)
        if no_output:
            return
        for line in output:
            self.msg("msg", line.decode().strip(), sender=self.name)
    
    def create_container(self) -> object:
        comp = self.docker.containers.create(
            image=self.DOCKER_IMAGE,
            command="sleep infinity",
            name=self.DOCKER_CONTAINER_NAME,
            volumes={
                self.HIVE_OUTPUT_DIR : {"bind" : self.DOCKER_DIR_HIVE, "mode" : "rw"},
            },
            detach=True
        )
        return comp
    
    def download_image(self) -> None:
        down_output = self.docker.api.pull(self.DOCKER_IMAGE, stream=True, decode=True)
        for line in down_output:
            if 'status' in line:
                self.msg("msg", f"Status: {line['status']}", sender=self.name)
            if 'progress' in line:
                self.msg("msg", f"Progress: {line['progress']}", sender=self.name)
            if 'id' in line:
                self.msg("msg", f"ID: {line['id']} - {line['status']} {line.get('progress', '')}", sender=self.name)
        self.msg("msg", "Downloading Complete", sender=self.name)
    
    def install(self) -> None:
        if self.status:
            self.msg("msg", f"Core: '{self.name}' is installed.", sender=self.name)
            return
        if not self.check_docker_image():
            self.msg("msg", "Start image downloads. This may take some time.", sender=self.name)
            self.download_image()
        self.msg("msg", "Builiding Compiler Container.....", sender=self.name)
        self.create_container()
        # self.build_lab()
        self.msg("msg", "Builiding complete.", sender=self.name)
    

    # old functions
    def build_lab(self) -> None:
        self.msg("msg", "[!!] Start of laboratory construction .... [!!]", sender=self.name)
        self.compiler.start()
        self.eCMD("apt update")
        self.eCMD("apt install nasm binutils -y")
        self.eCMD("apt install python3 -y")
        self.eCMD("apt install -y gcc-mingw-w64-i686")
        self.eCMD("apt install -y mingw-w64")
        self.msg("msg", "------ Install Modules ------", sender=self.name)
        self.msg("msg", ", ".join(self.master.PYTHON_PIP_LIBRARY_WINDOWS), sender=self.name)
        for mod in self.master.PYTHON_PIP_LIBRARY_WINDOWS:
            self.eCMD(f"wine python -m pip install {mod}")
        self.msg("msg", "Building laboratory complete. Stoping container ....", sender=self.name)
        self.compiler.stop()
    #################################################

    def updatePIP(self) -> None:
        self.msg("msg", "[!!] Upgrading laboratory..... [!!]", sender=self.name)
        self.compiler.start()
        if len(self.master.PIP.PIP) < 1:
            self.msg("error", "[!!] No extra modules to update. [!!]", sender=self.name)
            return
        for mod in self.master.PIP.PIP:
            self.msg("msg", f"<<-- Add {mod} -->>", sender=self.name)
            self.eCMD(f"wine python -m pip install {mod}")
        self.msg("msg", "Update complete. Stoping container....", sender=self.name)
        self.compiler.stop()
    
    def installCore(self) -> None:
        self.install()



