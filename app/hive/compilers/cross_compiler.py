import docker
import os
from typing import Union


class CrossComp:
    def __init__(self, master: object):
        self.name = "CrossComp"
        self.master = master
        self.msg = self.master.msg
        self.docker = docker.from_env()
        self.container_id = None

        # Hive output dir
        self.HIVE_OUTPUT_DIR = self.master.DIR_HIVE_OUT
        # dokcer hive directory
        self.DOCKER_DIR_HIVE = "/hive"
        # docker image
        self.DOCKER_IMAGE = "littleatarixe/wine_py:1.0"
        # docker container name
        self.DOCKER_CONTAINER_NAME = "crosscomp"
        # default DLL
        self.DEFAULT_DLL = "-lkernel32 -lmsvcrt -luser32 -lshell32 -lws2_32 -lshlwapi"
        self.STATIC_LINK = "-static-libstdc++ -static-libgcc"


    @property
    def status(self) -> bool:
        if self.get_compiler():
            return True
        else:
            return False
    
    @property
    def compiler(self) -> Union[object, None]:
        return self.get_compiler()

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
        if not self.check_docker_image():
            self.msg("msg", "Start image downloads. This may take some time.", sender=self.name)
            self.download_image()
        self.msg("msg", "Builiding Compiler Container.....", sender=self.name)
        self.create_container()
        self.build_lab()
        self.msg("msg", "Builiding complete.", sender=self.name)
    
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


    
    # Execute Command in docker conatiner
    def eCMD(self, command: str, no_output: bool = False) -> None:
        exec_id = self.docker.api.exec_create(self.compiler.id, f"bash -c '{command}'")
        output = self.docker.api.exec_start(exec_id, stream=True)
        if no_output:
            return
        for line in output:
            self.msg("msg", line.decode().strip(), sender=self.name)
    
    def compile_PyInstaller(self, raw: object) -> object:
        self.msg("msg", "Use PyInstaller.", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name}"
        cmd = "wine pyinstaller"
        if raw.compiler_ONE_FILE:
            cmd += " --onefile"
        if raw.compiler_EXE_SHOW == "GUI" or raw.compiler_EXE_SHOW == "gui":
            cmd += " --windowed"
        else:
            cmd += " --console"
        if raw.icon:
            cmd += f" --icon={raw.icon}"
        cmd += f" --name={raw.worm_name} {raw.src_file_name}"
        self.msg("dev", cmd, sender=self.name)
        self.compiler.start()
        self.eCMD(f"{enter_dir} && {cmd}")
        self.msg("msg", "Compile done.", sender=self.name)
        self.eCMD(f"{enter_dir} && cd dist && cp ./{raw.worm_name}.exe {self.DOCKER_DIR_HIVE}/{raw.worm_name}")
        self.eCMD(f"chmod 777 {self.DOCKER_DIR_HIVE}/{raw.worm_name}/{raw.worm_name}.exe")
        self.eCMD(f"{enter_dir} && rm -R build/")
        self.eCMD(f"{enter_dir} && rm -R dist/")
        self.compiler.stop()

        raw.exe_file_name = f"{raw.worm_name}.exe"
        if raw.ready_app:
            raw.ready_app_list.append(raw.exe_file_name)
        return raw
    
    
    def compile_nuitka_exe(self, raw: object) -> object:
        self.msg("msg", "Use Nuitka.", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name}"
        cmd = "wine python -m nuitka --onefile --mingw64"
        if raw.compiler_EXE_SHOW.lower() == "gui":
            cmd += f" --windows-icon-from-ico={raw.icon}"
        cmd += f" {raw.src_file_name}"
        self.msg("dev", cmd, sender=self.name)
        self.compiler.start()
        self.eCMD(f"{enter_dir} && {cmd}")
        self.msg("msg", "removing trash files...", sender=self.name)
        self.eCMD(f"{enter_dir} && rm -R {raw.worm_name}.build")
        self.eCMD(f"{enter_dir} && rm -R {raw.worm_name}.dist")
        self.eCMD(f"{enter_dir} && rm -R {raw.worm_name}.onefile-build")
        self.eCMD(f"{enter_dir} && chmod 777 {raw.worm_name}.exe")
        self.compiler.stop()
        raw.exe_file_name = f"{raw.worm_name}.exe"
        if raw.ready_app:
            raw.ready_app_list.append(raw.exe_file_name)
            

        return raw
    
    def compile_mingw_x64_exe(self, raw: object) -> object:
        self.msg("msg", "Use mingw-x64 compiler", sender=self.name)
        self.msg("msg", "Start compiler...", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name}"
        self.compiler.start()
        if raw.cscript:
            raw = self.build_res_cmd(raw)
            self.build_res_file(raw)
        cmd = f"nasm -f win64 {raw.src_file_name} -o {raw.worm_name}.o"
        self.msg("dev", cmd, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        cmd = "x86_64-w64-mingw32-gcc -m64"
        if raw.NO_STD_LIB:
            cmd += " -nostdlib -s"
        cmd += f" -o {raw.worm_name}.exe {raw.worm_name}.o"
        # res file
        if raw.cscript:
            cmd += f" {raw.cscript_res_name}"
        # build entry point
        if raw.compiler_EXE_SHOW == "gui":
            cmd += " -Wl,-e,WinMain"
        else:
            cmd += " -Wl,-e,main"
        
        # add static lib
        for sl in raw.lib_ADD_CMD:
            cmd += f" {sl}"

        # add default dll lib
        cmd += f" {self.DEFAULT_DLL}"
        # add dynamic dll lib
        for ddll in raw.dll_ADD_CMD:
            cmd +=f" {ddll}"

        if raw.compiler_EXE_SHOW == "gui":
            cmd += " -mwindows"
        
        self.msg("msg", f"Building worm: '{raw.worm_name}'...", sender=self.name)
        self.msg("dev", cmd, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        self.eCMD(f"{enter_dir} && chmod 777 *")
        self.msg("msg", "Stoping compiler...", sender=self.name)
        self.compiler.stop()

        raw.exe_file_name = f"{raw.worm_name}.exe"
        if raw.ready_app:
            raw.ready_app_list.append(raw.exe_file_name)
        return raw


    def compile_dll_module(self, rdll: object) -> object:
        match rdll.compiler_name:
            case "mingw-x32":
                cmd_comp = "i686-w64-mingw32-gcc"
                cmd_raw = "nasm -f win32"
            case "mingw-x64":
                cmd_comp = "x86_64-w64-mingw32-gcc"
                cmd_raw = "nasm -f win64"
            case _:
                self.msg("error", f"[!!] ERROR: Compiler: '{rdll.compiler_name}' is not supported [!!]", sender=self.name)
                rdll.raw_worm.last_error = 1
                return rdll
        self.msg("msg", f"Starting compilation '{rdll.raw_module.Name}' as '{rdll.out_file_name}'...", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{rdll.master_worm_name}"
        self.msg("msg", f"Start compiler {rdll.compiler_name}", sender=self.name)
        self.compiler.start()
        cmd_raw += f" {rdll.src_file_name} -o {rdll.raw_file_name}.o"
        self.msg("dev", cmd_raw, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd_raw}")
        cmd_comp += f" -shared {rdll.raw_file_name}.o {rdll.def_file_name}"
        cmd_comp += f" -o {rdll.out_file_name}"
        # add rc file

        # check NO_STD_LIB
        if rdll.raw_worm.NO_STD_LIB:
            cmd_comp += " -nostdlib -s"
        
        # add default library
        cmd_comp += f" {self.DEFAULT_DLL}"

        # add entry point
        cmd_comp += " -Wl,--entry=DllMain"

        self.msg("dev", cmd_comp, sender=self.name)
        self.msg("msg", "Builiding DLL file.....", sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd_comp}")
        self.eCMD(f"{enter_dir} && chmod 777 *")
        self.msg("msg", "Stoping compiler....", sender=self.name)
        self.compiler.stop()

        return rdll
    
    def compile_static_library(self, rlib: object) -> object:
        self.msg("msg", f"Starting compilation: {rlib.out_file_name} ...", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{rlib.master_worm_name}"
        self.msg("msg", f"Start compiler {rlib.compiler_name}", sender=self.name)
        self.compiler.start()
        cmd = f"nasm -f win64 {rlib.src_file_name} -o {rlib.raw_file_name}.o"
        self.msg("dev", cmd, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        cmd = f"x86_64-w64-mingw32-ar rcs {rlib.out_file_name} {rlib.raw_file_name}.o"
        self.msg("dev", cmd, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        self.msg("msg", "Stoping compiler....", sender=self.name)
        self.compiler.stop()
        return rlib
        
    
    def compile_cpp(self, raw: object) -> object:
        self.msg("msg", "Use mingw-x64-cpp compiler", sender=self.name)
        self.msg("msg", "Start compiler...", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name}"
        self.compiler.start()
        if raw.cscript:
            raw = self.build_res_cmd(raw)
            self.build_res_file(raw)
        cmd = f"x86_64-w64-mingw32-g++ -o {raw.worm_name}.exe {raw.src_file_name}"
        # add compiler script
        if raw.cscript:
            cmd += f" {raw.cscript_res_name}"
        # add sfiles
        for sf in raw.sfiles_ADD_CMD:
            cmd += f" {sf}" 
        
        # add static lib

        # add dll
        for dll in raw.dll_ADD_CMD:
            cmd += f" ./{dll}"
        # add default dll
        cmd += f" {self.DEFAULT_DLL}"

        cmd += f" {self.STATIC_LINK}"

        if raw.NO_STD_LIB:
            cmd += " -Os -s -Wl,--gc-sections"
        self.msg("dev", cmd, sender=self.name)
        self.msg("msg", f"Building worm: '{raw.worm_name}'...", sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        self.eCMD(f"{enter_dir} && chmod 777 *")
        self.msg("msg", "Stoping compiler....", sender=self.name)
        self.compiler.stop()
        return raw
    

    def compile_win_shellcode_x64(self, raw: object) -> object:
        self.msg("msg", "Use mingw-x64 compiler", sender=self.name)
        self.msg("msg", "Start compiler...", sender=self.name)
        enter_dir = f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name}"
        self.compiler.start()
        cmd = f"nasm -f bin {raw.src_file_name} -o {raw.worm_name}.o"
        self.msg("dev", cmd, sender=self.name)
        self.eCMD(f"{enter_dir} && {cmd}")
        self.eCMD(f"{enter_dir} && objdump -D -b binary -mi386:x86-64 {raw.worm_name}.o > {raw.worm_name}_objdump.txt", no_output=True)
        self.eCMD(f"{enter_dir} && chmod 777 *")
        raw.bin_file_name = f"{raw.worm_name}.o"
        raw.bin_file_path = os.path.join(raw.dir_out_main, raw.bin_file_name)
        self.msg("msg", "Stoping compiler....", sender=self.name)
        self.compiler.stop()
        return raw


    ########### Compiler script (res, rc file) ###################

    def build_res_cmd(self, raw: object) -> object:
        match raw.compiler_name:
            case "mingw-x64":
                raw.cscript_res_name = f"{raw.worm_name}.res"
                raw.cscript_CMD = f"x86_64-w64-mingw32-windres {raw.cscript_name} -O coff -o {raw.cscript_res_name}"
            case "mingw-x64-cpp":
                raw.cscript_res_name = f"{raw.worm_name}.res"
                raw.cscript_CMD = f"x86_64-w64-mingw32-windres {raw.cscript_name} -O coff -o {raw.cscript_res_name}"
            case _:
                return raw

        return raw

    def build_res_file(self, raw: object) -> None:
        self.msg("msg", "Building res file....", sender=self.name)
        self.eCMD(f"cd {self.DOCKER_DIR_HIVE}/{raw.worm_name} && {raw.cscript_CMD}")
