import os

from configparser import ConfigParser
from typing import Union
from threading import Lock
from pathlib import Path


class Builder:
    def __init__(self):
        self.DIR_MAIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.DIR_HIVE = os.path.join(self.DIR_MAIN, "app", "hive")
        self.DEFAULT_CONFIG = os.path.join(self.DIR_MAIN, "CONFIG.ini")
        self.DEFAULT_DEV_CONFIG = os.path.join(self.DIR_MAIN, "dev_conf.ini")
        self.DIR_SYS_FILES = os.path.join(self.DIR_MAIN, "app", "_sys_files")
        self.FD_SOCKET_DRACO_MSG = os.path.join(self.DIR_SYS_FILES, "draco.msg")
        self.FD_SOCKET_DRACO_CONTROLER = os.path.join(self.DIR_SYS_FILES, "draco.ctrl")
        self.DIR_OUTPUT = os.path.join(self.DIR_MAIN, "OUTPUT")
        self.DIR_LOGS = os.path.join(self.DIR_OUTPUT, "Logs")
        self.DIR_HIVE_OUT_RAW = os.path.join(self.DIR_OUTPUT, "Hive")
        self.DIR_INPUT = os.path.join(self.DIR_MAIN, "INPUT")
        self.DIR_SHORTCUTS = os.path.join(self.DIR_OUTPUT, "Links")

        # Loot dir
        self.DIR_LOOT = os.path.join(self.DIR_OUTPUT, "Loot")

        # path to the 'hive' directory in the docker image
        self.DIR_HIVE_IN_DOCKER_IMAGE = "/hive"

        self.DRACONUS_LOCK_FILE_NAME = "draconus.lock"

        ### make log file Lock
        self.LOCK_TH_DRACONUS_LOGS = Lock()

        ### messanger default table style
        self.MSG_DEFAULT_TABLE_STYLE = "simple"
        self.MSG_FIRST_TABLE_SPACE = "+ "

        #### messanger pause send msg
        self.MSG_PAUSE_UNIX_SEND = 0.1
        self.MSG_UNIX_SEPARATOR = "####"

        
        self.read_conf()
        self.make_dirs()
    
    def read_conf(self) -> None:
        conf = ConfigParser()
        conf.read(self.DEFAULT_CONFIG)
        basic = conf["CONFIG"]
        console_scr = self.make_console_screen(basic.get("CONSOLE_SCREEN"))
        ### BASIC SETTINGS
        main = {
            "ip" : basic.get("IP"),
            "unix_socket_raw_len" : int(basic.get("unix_socket_raw_len")),
            "unix_socket_format" : basic.get("unix_socket_format"),
            "tcp_socket_format" : basic.get("tcp_socket_format"),
            "tcp_socket_raw_len" : int(basic.get("tcp_socket_raw_len")),
            "tcp_socket_download_raw_len" : int(basic.get("tcp_socket_download_raw_len")),
            "vanilla_print" : basic.getboolean("vanilla_print"),
            "show_no_important_messages" : basic.getboolean("show_no_important_messages"),
            "unix_socket_separator" : basic.get("unix_socket_separator"),
            "tcp_socket_separator" : basic.get("tcp_socket_separator"),
            "sender_socket_to" : 60,
            "tcp_raw_buffer_to" : int(basic.get("TCP_RAW_BUFFER_TIMEOUT")),
            "console_screen" : console_scr,
            "draconus_logs_file_name" : basic.get("DRACONUS_LOGS_FILE_NAME"),
            "hive_logs_file_name" : basic.get("HIVE_LOGS_FILE_NAME"),
            "msg_color_basic" : basic.get("BASIC_MSG"),
            "msg_color_no_imp" : basic.get("NO_IMP_MSG"),
            "msg_color_error" : basic.get("ERROR_MSG"),
        }

        ### DEV SETTINGS
        dev = conf["DEV"]
        dconf = {
            "task_pause_clean" : float(dev.get("task_pause_clean")),
            "dev_msg" : dev.getboolean("dev_msg"),
            "tcp_sock_to_listening" : int(dev.get("tcp_socket_timeout_listening")),
            "unix_sock_to_recive" : int(dev.get("unix_socket_timeout_recive")),
            "tcp_sock_to_recive" : int(dev.get("tcp_socket_timeout_recive")),
            "central_clean_pause" : int(dev.get("central_cleaner_time_pause")),
            "msg_color_dev" : dev.get("DEV_MSG_COLOR"),
            "dev_mode" : dev.getboolean("DEV_MODE")
        }

        ### update directories
        self.PATH_DRACONUS_LOGS = os.path.join(self.DIR_LOGS, main["draconus_logs_file_name"])
        self.PATH_HIVE_LOGS = os.path.join(self.DIR_LOGS, main["hive_logs_file_name"])
        

        self.TCP_RAW_BUFFER_TIMEOUT = int(basic.get("TCP_RAW_BUFFER_TIMEOUT"))
        
        self.DEFAULT_COMPILER_CORE = basic.get("DEFAULT_COMPILER_CORE")
        self.COMPILER_CONTAINER_NAME = basic.get("COMPILER_CONTAINER_NAME")
        self.HIVE_OUTPUT_WORM_DIR_NAME = basic.get("HIVE_OUTPUT_WORM_DIR_NAME")
        self.DEFAULT_LINKER_DLL = self._build_dll_list(basic.get("DEFAULT_LINKER_DLL"))

        self.DIR_HIVE_OUT = os.path.join(Path.home(), self.HIVE_OUTPUT_WORM_DIR_NAME)

        main.update(dconf)
        self.update_config(main)

        


    
    def update_config(self, conf: dict) -> None:
        for k, i in conf.items():
            setattr(self, k, i)

    
    def make_console_screen(self, char_count: int) -> dict:
        try:
            char_count = int(char_count)
        except Exception as e:
            print("ERROR convert screen size. Use default.\nERROR: ", e)
            char_count = 120
        if char_count < 120:
            char_count = 120
        d_col1 = 25
        d_col2 = 25
        d_col3 = 30
        d_col4 = char_count - d_col1 - d_col2 - d_col3
        scr = {
            "4c" : (d_col1, d_col2, d_col3, d_col4),
            "3c" : (d_col1, d_col2, d_col3 + d_col4),
            "2c" : (d_col1, d_col4 + d_col2),
            "slen" : char_count
        }

        return scr

    def make_dirs(self) -> None:
        draco_dirs = [
            self.DIR_SYS_FILES,
            self.DIR_OUTPUT,
            self.DIR_LOGS,
            self.DIR_HIVE_OUT,
            self.DIR_INPUT,
            self.DIR_SHORTCUTS,
            self.DIR_LOOT
        ]

        for d in draco_dirs:
            self._make_dir(d)

    def _make_dir(self, fpath: str) -> None:
        if os.path.exists(fpath):
            return
        else:
            try:
                os.mkdir(fpath)
            except Exception as e:
                print("ERROR: while creating directories: ", e)


    def _build_dll_list(self, dlls: str) -> list:
        dll_list = []
        for d in dlls.split(","):
            if d == "" or d == " ":
                continue
            dll_list.append(d)
        return dll_list


