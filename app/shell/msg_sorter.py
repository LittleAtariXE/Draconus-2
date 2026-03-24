
from termcolor import cprint
from tabulate import tabulate

from ..tools.builder import Builder

class MessageSorter:
    def __init__(self, builder_object: Builder):
        self.CONF = builder_object

        self.CONSOLE_SCR = self.CONF.console_screen
        self.DEFAULT_SORT_TEXT_LEN_FIRST = 40
        self.SORT_TEXT_LEN_FIRST = self.DEFAULT_SORT_TEXT_LEN_FIRST
        self.SORT_TEXT_LEN_SECOND = self.CONSOLE_SCR["slen"] - self.SORT_TEXT_LEN_FIRST - 10


        self.colors = {
            "cmd_name" : "blue",
            "cmd_info" : "green",
            "title" : "white",
            "btext" : "yellow",
            "error" : self.CONF.msg_color_error,
        }
    
    def set_text_len_first(self, value: int) -> None:
        self.SORT_TEXT_LEN_FIRST = value
        self.SORT_TEXT_LEN_SECOND = self.CONSOLE_SCR["slen"] - self.SORT_TEXT_LEN_FIRST - 10
    
    def restore_text_len_first(self) -> None:
        self.SORT_TEXT_LEN_FIRST = self.DEFAULT_SORT_TEXT_LEN_FIRST
        self.SORT_TEXT_LEN_SECOND = self.CONSOLE_SCR["slen"] - self.SORT_TEXT_LEN_FIRST - 10

    def sort_Text(self, func_name: str, func_description: str) -> None:
        cprint(f"\t{func_name}", self.colors["cmd_name"], end="")
        sep = self.SORT_TEXT_LEN_FIRST - len(func_name)
        cprint(f"{'':{sep}}{func_description}", self.colors["cmd_info"])
    
    def make_Title(self, text: str) -> None:
        sep = self.CONSOLE_SCR["slen"] - 25
        title = f"  {text}  "
        title_len = len(title)
        sep = int((sep - title_len) / 2 )
        title = "+" * sep + title + "+" * sep
        cprint(title, self.colors["title"])
    
    def basic_Text(self, text: str, tab_num: int = 1) -> None:
        tab = "\t" * tab_num
        cprint(f"{tab}{text}", self.colors["btext"])
    
    def message_error(self, text: str) -> None:
        cprint(text, self.colors["error"])
    