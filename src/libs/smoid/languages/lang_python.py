import re

from smoid.languages import Check, CheckCollection


class PythonClassDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Python:Class/Declaration"
        self.example = "class CoolClass:"
        self.add_language("python")

        res_name = "(?:[a-zA-Z_][a-zA-Z0-9_]*)"
        res_full_name = res_name + "(?:\." + res_name + ")*"

        res_class = "\s*class\s+" + res_name + "\s*"
        res_class += "(\(\s*" + res_full_name + "\s*\))?\s*:"

        self.add_multiple_matches(res_class, 50)


class PythonInitMethodCheck(Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Python:InitMethod"
        self.add_language("python")
        self.add_multiple_matches("\s+def\s+__init__\s*\(\s*self\s*,", 40)


class PythonImportCheck(Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Python:Import"
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
