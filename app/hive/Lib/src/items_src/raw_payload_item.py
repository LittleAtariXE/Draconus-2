from .raw_lib_item import RawLibItem

class RawPayloadLibItem(RawLibItem):
    def __init__(self, raw_info_item: object):
        super().__init__(raw_info_item)

        # Path to main OUTPUT directory in HIVE
        self.DIR_HIVE_OUTPUT = None

        # Path to the file with ready data
        self.PATH_FILE_DATA = None

        # Write payload code
        # Determines whether the PAYLOAD code should be saved.
        # This is needed if PAYLOAD is to be compiled.
        self.payloadCodeWrite = False


    def updateConfig(self, conf: dict) -> None:
        self.DIR_HIVE_OUTPUT = conf.get("DIR_HIVE_OUTPUT")
