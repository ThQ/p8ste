# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It  is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.

import re

import check


class PythonClassDeclarationCheck (check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "Class declaration (class * (*):)"

    def _test(self):
        result = False
        re_class = "(?:[a-zA-Z_][a-zA-Z0-9_]*)"
        re_class_full = re_class + "(?:\." + re_class + ")*"
        if self.is_re_found("\s*class\s+" + re_class + "\s*\(\s*" + re_class_full + "\s*\)\s*:\s*") :
            self.probability = 50
            result = True
        return result

class PythonSourceEncodingCheck(check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "Source encoding (# -*- coding: * -*-)"

    def _test(self):
        result = False
        if self.is_re_found("\s*# -\*- coding: [a-zA-Z0-9]+ -\*-") :
            self.probability = 50
            result = True
        return result


class PythonInitMethodCheck(check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "__init__ method"

    def _test(self):
        result = False
        if self.is_re_found("\s+def\s+__init__\s*\(\s*self\s*,") :
            self.probability = 50
            result = True
        return result

class PythonHeaderCheck(check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "Header (#!.../pyton)"

    def _test(self):
        result = False
        if self.is_re_matched("#!/(.+)python(\n|$)") :
            self.probability = 60
            result = True
        return result

class PythonImportCheck(check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "Imports"

    def _test(self):
        result = False
        # (^|\n)\s*(from\s+[a-zA-Z_.]\s+)?
        if self.is_re_found("import(\s+[a-zA-Z_.]+)((\s*,\s*[a-zA-Z_.]+)+)?(\n|\r)") :
            self.probability = 60
            result = True
        return result

class PythonCheck (check.LanguageCheck):
    def __init__(self):
        check.LanguageCheck.__init__ (self)
        self.name = "python"
        self.checkers.append(PythonHeaderCheck())
        self.checkers.append(PythonImportCheck())
        self.checkers.append(PythonClassDeclarationCheck())
        self.checkers.append(PythonInitMethodCheck())
        self.checkers.append(PythonSourceEncodingCheck())


