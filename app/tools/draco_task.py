
import threading
from time import sleep
from typing import Union, Callable

from .builder import Builder


class DracoTask:
    def __init__(self,
            name: str,
            thread: object,
            info: str = "",
            th_type: str = "system",
    ):
        self.name = name
        self.thread = thread
        self.info = info
        self.th_type = th_type
    
    @property
    def is_alive(self) -> bool:
        if self.thread.is_alive():
            return True
        else:
            return False
    
    def startTH(self) -> bool:
        if self.is_alive:
            return False
        self.thread.start()
        return True

    




class Tasker:
    def __init__(self, draconus: object, builder_object: Builder):
        self.draconus = draconus
        self.CONF = builder_object
        self.msg = self.draconus.msg
        self.th_lock = threading.Lock()
        self.dTH = {}

        self.PAUSE_TASK_CLEAN = 1
        self.CONSOLE_SCR = self.CONF.console_screen
    
    @property
    def FLAG_working(self) -> bool:
        return self.draconus.FLAG_working
    

    def addWorkingThread(self, name: str, thread: object, info: str = "", th_type: str = "system") -> None:
        nth = DracoTask(name, thread, info, th_type)
        with self.th_lock:
            self.dTH[nth.name] = nth
    
    def addThread(self, name: str, func_name: Callable, fargs: tuple = (), info: str = "", th_type: str = "system", daemon: bool = False, start_now: bool = True) -> None:
        thread = threading.Thread(target=func_name, args=fargs, daemon=daemon)
        nth = DracoTask(name, thread, info, th_type)
        if start_now:
            nth.startTH()
        with self.th_lock:
            self.dTH[nth.name] = nth
        

    def showTasks(self) -> None:
        tab = {}
        tab["headers"] = ["Name:", "Types:", "Is working:", "Description:"]
        tab["data"] = []
        for th in self.dTH.values():
            tab["data"].append([th.name, th.th_type, f" {str(th.is_alive)} ", th.info])
        tab["width"] = self.CONSOLE_SCR["4c"]
        self.msg("msg", "  Active Tasks:  ", mtypes="title")
        self.msg("msg", tab, mtypes="table", no_separator=True)
    

    def cleaner(self) -> None:
        while self.FLAG_working:
            too_clean = []
            for th in self.dTH.values():
                if not th.is_alive:
                    too_clean.append(th.name)
            with self.th_lock:
                for c in too_clean:
                    try:
                        del self.dTH[c]
                    except KeyError:
                        pass
            sleep(self.PAUSE_TASK_CLEAN)
    
    def Start(self) -> None:
        self.addThread("TaskCleaner", self.cleaner, info="Deletes inactive threads and tasks.", daemon=True)
    

