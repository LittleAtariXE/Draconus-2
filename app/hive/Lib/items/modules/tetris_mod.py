#!name##TMod
#!itemType##module
#!fileType##PY_MOD
#!info##Tetris test module
#!hiveType##PySM
#!lang##python
#!pyModName##Kaloryfer

from time import sleep


class Kaloryfer:
    MTYPES = "rat"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
    
    def work(self) -> None:
        while self.worm.FLAG_working:
            sleep(0.5)
            # print("Kaloryfer working")
            # self.worm.processData("wclose")
        print("Kaloryfer END")
    
    def start(self) -> None:
        print("Kaloryfer start")
        self.work()