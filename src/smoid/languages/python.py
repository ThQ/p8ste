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
        self.add_language("python")
        self.add_multiple_matches("import(\s+[a-zA-Z_.]+)((\s*,\s*[a-zA-Z_.]+)+)?(\n|\r)", 40)


class PythonCheck (CheckCollection):
    def __init__(self):
        self.name = "python"
        self.append(PythonClassDeclarationCheck())
        self.append(PythonImportCheck())
        self.append(PythonInitMethodCheck())
