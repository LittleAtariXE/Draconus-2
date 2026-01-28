
from termcolor import cprint
from .builder import Builder


class Messages:
    def __init__(self, builder_object: object, sender_name: str = "Commander") -> None:
        self.CONF = builder_object
        self.sender_name = sender_name

        self.color_error = self.CONF.msg_color_error
        self.color_basic = self.CONF.msg_color_basic
    

    def msgError(self, text: str, sender: str = None) -> None:
        if not sender:
            sender = self.sender_name
        
        cprint(f"[{sender}] {text}", self.color_error)
    
    def msgBasic(self, text: str, sender: str = None) -> None:
        if not sender:
            sender = self.sender_name
        cprint(f"[{sender}] {text}", self.color_basic)
    
    