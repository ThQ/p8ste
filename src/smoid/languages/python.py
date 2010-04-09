import re

from smoid.languages import Check, CheckCollection


class PythonClassDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "PythonClassDeclaration"
        self.example = "class CoolClass:"
        self.add_language("python")
        re_class = "(?:[a-zA-Z_][a-zA-Z0-9_]*)"
        re_class_full = re_class + "(?:\." + re_class + ")*"
        self.add_multiple_matches("\s*class\s+" + re_class + "\s*(\(\s*" + re_class_full + "\s*\))?\s*:", 50)


class PythonInitMethodCheck(Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "PythonInitMethod"
        self.add_language("python")
        self.add_multiple_matches("\s+def\s+__init__\s*\(\s*self\s*,", 40)


class PythonImportCheck(Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "PythonImport"
        self.example = "from subprocess import Popen, PIPE"
        self.add_language("python")

        res_class = "[a-zA-Z][a-zA-Z0-9_]*"
        res_full_class = res_class + "(\." + res_class + ")*"
        res_class_list = res_class + "(\s*,\s*" + res_class + ")*"
        self.add_multiple_matches("from\s+" + res_full_class + "\s+import\s+" + res_class_list + "\s*(\n|\r|;)", 40)


class PythonCheck (CheckCollection):
    def __init__(self):
        self.name = "python"
        self.append(PythonClassDeclarationCheck())
        self.append(PythonImportCheck())
        self.append(PythonInitMethodCheck())
