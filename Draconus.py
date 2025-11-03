import os


from app.draconus import Draconus
from app.tools.builder import Builder




from time import sleep


if __name__ == "__main__":
    bconf = Builder()
    draco = Draconus(bconf)
    draco.Start()
    

