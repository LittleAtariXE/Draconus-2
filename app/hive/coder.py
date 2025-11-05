from __future__ import annotations
import os
import sys

from typing import Union
from jinja2 import Template

from .template_tools.nasm_builder import NasmBuilderTemplate
from .template_tools.temp_random import RandomTemplate
from .template_tools.temp_shadow import ShadowTemplate
from .template_tools.py_temp import PyTemplate

from .raw_worm_builder import RawWormBuilder




class NasmCoder:
    def __init__(self, coder: Coder, output_work_dir: str):
        self.coder = coder
        self.name = self.coder.name
        self.msg = self.coder.msg
        self.output_dir = output_work_dir
        # file path : raw code
        self.raw_code = {}
    
    def addCode(self, raw_code: str, code_file_name: str) -> None:
        fpath = os.path.join(self.output_dir, code_file_name)
        rcode = self.raw_code.get(fpath)
        if rcode:
            self.raw_code[fpath] += raw_code
        else:
            self.raw_code[fpath] = raw_code


class CppCoder:
    def __init__(self, coder: Coder, output_work_dir: str):
        self.coder = coder
        self.name = self.coder.name
        self.msg = self.coder.msg
        self.output_dir = output_work_dir
        # file path : raw code
        self.raw_code = {}
    
    def addCode(self, raw_code: str, code_file_name: str) -> None:
        fpath = os.path.join(self.output_dir, code_file_name)
        self.raw_code[fpath] = raw_code

class PythonCoder:
    def __init__(self, coder: Coder, output_work_dir: str):
        self.coder = coder
        self.name = self.coder.name
        self.msg = self.coder.msg
        self.output_dir = output_work_dir
        self.std_lib = sys.stdlib_module_names

        self.py_import = set()
        self.pip_import = set()
        self._raw_code = {
            "master" : [],
            "module" : [],
            "loader" : [],
        }
    
    @property
    def raw_code(self) -> str:
        return self.oneFile

    @property
    def oneFile(self) -> str:
        return self.merge_code()

    def merge_code(self) -> str:
        code = ""
        for lod in self._raw_code["loader"]:
            code += lod
        code += "\n\n"
        for imp in self.py_import:
            code += imp + "\n"
        code += "\n"
        for mod in self._raw_code["module"]:
            code += mod + "\n"
        code += "\n"
        for mas in self._raw_code["master"]:
            code += mas + "\n"
        return code
        
    
    def addCode(self, raw_code: str, mod_type: str = None, hold_import: bool = False) -> None:
        if not mod_type:
            mod_type = "master"
        code = self.add_import(raw_code, hold_import)
        self._raw_code[mod_type].append(code)
        self.msg("dev", f"Add Python {mod_type} code.", sender=self.name)
    
    def add_import(self, raw_code: str, hold_import: bool = False) -> str:
        if hold_import:
            return raw_code
        code = ""
        rcode = raw_code.split("\n")
        for line in rcode:
            if line == "\n" or line == "":
                continue
            if line.startswith("import") or line.startswith("from"):
                self.py_import.add(line)
                imp = line.split(" ")
                self.check_std_lib(imp[1])
            else:
                code += line + "\n"
        return code
    
    def check_std_lib(self, mod_name: str) -> None:
        if not mod_name in self.std_lib:
            self.pip_import.add(mod_name)
    

    
    
            


    




class Coder:
    def __init__(self, queen: object, raw_worm_builder: RawWormBuilder):
        self.name = "Coder"
        self.queen = queen
        self.msg = self.queen.msg
        self.raw_builder = raw_worm_builder

        # Template tools
        self.TEMP_shadow = ShadowTemplate(self)
        self.TEMP_nasm = NasmBuilderTemplate(self)
        self.TEMP_random = RandomTemplate(self)
        self.TEMP_python = PyTemplate(self)

    
    def _build_extra_var(self) -> dict:
        extra = {}
        extra["_WORM_NAME"] = self.raw_builder.wormName
        extra["_PY_IMPORT"] = []
        extra["_PY_PIP_IMPORT"] = []
        extra["_PY_MODULES"] = []
        extra["_ICON_NAME"] = self.raw_builder.Icons.icon
        return extra

    def buildVariable(self) -> dict:
        var = self._build_extra_var()
        for v in self.raw_builder.RAW.variables.values():
            var[v.name] = v.value
        # add NULL payload variables
        for name in self.raw_builder.RAW.payloads.keys():
            var[name] = None
        # add FOOD variables
        for fname, food in self.raw_builder.RAW.food.items():
            var[fname] = food.Value
        return var
    
    def renderSingleTemplate(self, code: str, var: dict = {}) -> str:
        try:
            fcode = Template(code)
            fcode = fcode.render(**var, shTOOL=self.TEMP_shadow, asmTOOL=self.TEMP_nasm, randTOOL=self.TEMP_random, pyTOOL=self.TEMP_python)
            return fcode
        except Exception as e:
            self.msg("error", f"[!!] ERROR: render template: {e} [!!]", sender=self.name)
            return code
    

    def buildNasmCode(self, raw_lib_item_list: list, work_output_dir: str, master_file_name: str) -> dict:
        nasm_code = NasmCoder(self, work_output_dir)
        nasm_lang = ["nasm", "asm"]
        for rl in raw_lib_item_list:
            if rl.lang.lower() in nasm_lang:
                if rl.supportFileCodeName:
                    nasm_code.addCode(rl.raw_code, rl.supportFileCodeName)
                else:
                    nasm_code.addCode(rl.raw_code, master_file_name)
        return nasm_code.raw_code
    
    def buildCppCode(self, raw_lib_item_list: list, work_output_dir: str, master_file_name: str) -> dict:
        cpp_code = CppCoder(self, work_output_dir)
        for rl in raw_lib_item_list:
            if rl.supportFileCodeName:
                cpp_code.addCode(rl.raw_code, rl.supportFileCodeName)
            else:
                cpp_code.addCode(rl.raw_code, master_file_name)
        return cpp_code.raw_code

    def buildPythonCode(self, raw_lib_item_list: list, work_output_dir: str, master_file_name: str) -> tuple(list, str):
        py_code = PythonCoder(self, work_output_dir)
        for rl in raw_lib_item_list:
            if rl.lang:
                if rl.lang.lower() == "python":
                    py_code.addCode(rl.raw_code, rl.pyType, rl.pyImportHold)
        
        fpath = os.path.join(work_output_dir, master_file_name)
        py_data = {}
        py_data["fpath"] = fpath
        py_data["raw_code"] = py_code.oneFile
        py_data["pip_import"] = list(py_code.pip_import)
        py_data["py_import"] = list(py_code.py_import)
        
        return py_data
    