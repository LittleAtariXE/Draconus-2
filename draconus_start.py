import os

from app.draconus import Draconus
from app.tools.builder import Builder



if __name__ == "__main__":
    bconf = Builder()
    draco = Draconus(bconf)
    draco.Start()