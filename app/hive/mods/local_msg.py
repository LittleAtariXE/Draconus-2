import os
from threading import Lock
from termcolor import cprint
from datetime import datetime

from tabulate import tabulate
from typing import Union


# MSG_STANDARD_MSG = "yellow"
# MSG_ERROR_MSG = "red"
# MSG_NO_IMP_MSG = "yellow"
MSG_DEV_MSG = "blue"
MSG_DEFAULT_TABLE_STYLE = "simple"
MSG_DEFAULT_TABLE_FIRST_SPACE = 4

# MSG_LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "logs.txt")
# MSG_LOG_FILE_PATH2 = os.path.join(os.path.dirname(__file__), "logs_hive.txt")

class LocalMSG:
    def __init__(self, queen: object):
        self.queen = queen
        self.console_scr = self.queen.conf.console_screen
        self.show_no_imp_msg = True
        self.show_dev_msg = True
        self.log_draco_file_path = self.queen.conf.PATH_DRACONUS_LOGS
        self.log_hive_file_path = self.queen.conf.PATH_HIVE_LOGS
        self.lock = Lock()
        self.colors = {
            "msg" : self.queen.conf.msg_color_basic,
            "error" : self.queen.conf.msg_color_error,
            "no_imp" : self.queen.conf.msg_color_no_imp,
            "dev" : MSG_DEV_MSG
        }
        self.first_table_space = "+ "
        self.make_log_file()
    
    @property
    def date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def make_log_file(self) -> None:
        if not os.path.exists(self.log_hive_file_path):
            with open(self.log_hive_file_path, "w") as file:
                file.write(f"START LOG FILE: {self.date}\n")
                file.write("-" * 100 + "\n\n")
        if not os.path.exists(self.log_draco_file_path):
            with open(self.log_draco_file_path, "w") as file:
                file.write(f"START LOG FILE: {self.date}\n")
                file.write("-" * 100 + "\n\n")
    
    def add_log_txt(self, msg: str, sender: str, draco_log: bool = False, no_separator: bool = False) -> None:
        with self.lock:
            with open(self.log_hive_file_path, "a+") as file:
                if no_separator:
                    file.write(msg + "\n")
                else:
                    file.write("-" * 100 + "\n")
                    file.write(f"[{self.date}][{sender}] {msg}\n")
            if draco_log:
                with open(self.log_draco_file_path, "a+") as file:
                    if no_separator:
                        file.write(msg + "\n")
                    else:
                        file.write("-" * 100 + "\n")
                        file.write(f"[{self.date}][{sender}] {msg}\n")
    
    def show_msg(self, types: str, msg: str, sender: str = "Queen", color: str = None, no_separator: bool = False) -> None:
        if types == "empty":
            print("\n")
            return
        if not color:
            color = self.colors.get(types)
        if types == "no_imp" and not self.show_no_imp_msg:
            return
        if types == "dev" and not self.show_dev_msg:
            return
        if no_separator:
            cprint(f"{msg}", color)
        else:
            cprint(f"[{sender}] {msg}", color)
    

    def process_msg(self, msg: Union[str, dict, list], mtypes: str = None, no_separator: bool = False) -> str:
        if mtypes:
            match mtypes:
                case "unpack":
                    msg = self._unpack_data_msg(msg)
                case "table":
                    msg = self._build_table(msg, no_separator)
                case "title":
                    msg = self._build_title(msg, no_separator)
        return msg
    
    def work(self, types: str, msg: Union[str, list, dict], sender: str = "Queen", mtypes: str = None, color: str = None, extCONF: dict = {}, draco_log: bool = False, no_separator: bool = False) -> None:
        msg = self.process_msg(msg, mtypes, no_separator)
        self.show_msg(types, msg, sender, color, no_separator)
        self.add_log_txt(msg, sender, draco_log, no_separator)

    def __call__(self, types: str, msg: Union[str, list, dict] = "", sender: str = "Queen", mtypes: str = None, color: str = None, extCONF: dict = {}, draco_log: bool = False, no_separator: bool = False) -> None:
        self.work(types, msg, sender, mtypes, color, extCONF, draco_log, no_separator)

    def _unpack_data_msg(self, msg: Union[dict, list]) -> str:
        data = ""
        if isinstance(msg, dict):
            for k,i in msg.items():
                data += f"{k} - {i}\n"
        elif isinstance(msg, list):
            for i in msg:
                data += f"{i}\n"
        else:
            data = str(msg)
        return data
    

    def _build_table(self, msg: dict, no_separator: bool = False) -> str:
        # data - list
        # headers - list
        # width - list
        # types - str tableFMT
        headers = msg.get("headers", [])
        data = msg.get("data", [])
        # add space to first element
        for d in data:
            d[0] = f"{self.first_table_space}{d[0]}"
        width = msg.get("width")
        if not isinstance(width, list):
            width = list(width)
        types = msg.get("types", MSG_DEFAULT_TABLE_STYLE)
        table = tabulate(data, headers=headers, tablefmt=types, maxcolwidths=width, disable_numparse=True)
        if no_separator:
            return table
        else:
            return "\n" + table
    
    def _build_title(self, msg: Union[str, list, dict], no_separator: bool = False) -> str:
        if not isinstance(msg, str):
            msg = str(msg)
        ltitle = self.console_scr["slen"] - len(msg)
        ltitle = int((ltitle / 2) - 10)
        ltitle = "*" * ltitle
        msg = f"{ltitle}{msg}{ltitle}"
        if no_separator:
            return msg
        else:
            return "\n" + msg

