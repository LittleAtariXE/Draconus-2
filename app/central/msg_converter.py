from __future__ import annotations

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .central import Central, ClientHandler



class MessageProcessor:
    def __init__(self, central: Central):
        self.central = central
        self.CONF = self.central.CONF
        self.msg = self.central.msg
        self.Tasker = self.central.Tasker
    

    