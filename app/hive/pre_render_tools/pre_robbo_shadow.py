from random import randint, choice
import string

class RobboShadow:
    def __init__(self, pre_master: object):
        self._key = "aaaa"
        self.power = 34
        self.key = self.build_key(self._key)
        self._trash_length = 5
        self._trash_count = 2

        self.char_key = string.ascii_letters
        self.Robbo = None


    def Build(self, *args) -> None:
        if len(args) > 0:
            self._key = args[0]
        else:
            self._key = "aaaa"
        if len(args) > 1:
            self.power = int(args[1])
        else:
            self.power = 34
        if len(args) > 2:
            self._trash_length = int(args[2])
        if len(args) > 3:
            self._trash_count = int(args[3])

        self.key = self.build_key(self._key)
        self.Robbo = self

    def ShowKey(self) -> str:
        key = [hex(c) for c in self.key]
        return ", ".join(key)
    
    def ShowPower(self, char: str = "#") -> str:
        return char * self.power

    def EncodeStr(self, text: str, add_zero: bool = True, add_trash: bool = True) -> str:
        return self.encode_str(text, add_zero, add_trash)
    
    def EncodeList(self, text: str, separator: str, add_zero: bool = True, add_trash: bool = True) -> str:
        rlist = []
        for line in text.split(separator):
            rlist.append("{" + self.encode_str(line.strip(), add_zero, add_trash) + "}")
        return ",\n".join(rlist)


    def gen_trash_name(self) -> list:
        length = self._trash_length
        count = self._trash_count
        code = []
        for _ in range(count):
            ki = 0
            i = 0
            size = randint(length, length * 2)
            while i < size:
                if ki == len(self.key):
                    ki = 0
                char = ord(choice(self.char_key))
                code.append(hex(char + (self.key[ki] * self.power)))
                i += 1
                ki += 1
            code.append("0x00")
        return code
    
    def build_key(self, key: str) -> list:
        return [ord(c) for c in key]
    
    def show_key(self) -> str:
        key = [hex(c) for c in self.key]
        print(", ".join(key))
    
    def show_power(self, char: str = "#") -> None:
        print(char * self.power)

    def encode_str(self, text: str, add_zero: bool = True, add_trash: bool = True) -> str:
        dig_text = [ord(c) for c in text]
        raw_text = []
        i = 0
        for x in dig_text:
            if i == len(self.key):
                i = 0
            raw_text.append(x + (self.key[i] * self.power))
            i += 1
        out_text = [hex(c) for c in raw_text]
        if add_zero:
            out_text.append("0x00")
        if add_trash:
            out_text.extend(self.gen_trash_name())
        return ", ".join(out_text)


