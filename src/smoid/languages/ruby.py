# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.


from smoid.languages import Check, LanguageCheck


class RubyClassDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Class declaration"

    def _test(self):
        result = False
        re_class = "[a-zA-Z_][a-zA-Z_0-9]+"
        if self.is_re_found("(^|\r|\n)\s*class\s+" + re_class + "\s*<<?\s*" + re_class + "\s*(\r|\n|$)") :
            self.probability = 40
            result = True
        return result


class RubyFunctionDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Function declaration"

    def _test(self):
        result = False
        re_class = "[a-zA-Z_][a-zA-Z_0-9]+"
        if self.is_re_found("(^|\r|\n)\s*def\s+(self\.)?[a-zA-Z_][a-zA-Z_0-9]*(!|\?)?"):
            self.probability = 40
            result = True
        return result


class RubyHeaderCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Headers"

    def _test(self):
        result = False
        if self.is_re_matched("^#!/(.+)ruby(\n|$)") :
            self.probability = 60
            result = True
        return result


class RubyModuleDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Module declaration"

    def _test(self):
        result = False
        re_class = "[a-zA-Z_][a-zA-Z_0-9]+"
        if self.is_re_found("(^|\r|\n)\s*module\s+[a-zA-Z_][a-zA-Z_0-9]*"):
            self.probability = 40
            result = True
        return result


class RubyRequireCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Require"

    def _test(self):
        result = False
        if self.is_re_found("(^|\n|\r)\s*require\s+'[^']+'\s*(\r|\n|$)") :
            self.probability = 40
            result = True
        return result


class RubyStrangeFunctionNamesCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Strange function names"

    def _test(self):
        result = False
        if self.is_re_found("\.[a-zA-Z_][a-zA-Z_0-9](\?|!)") :
            self.probability = 20
            result = True
        return result


class RubyCheck (LanguageCheck):
    def __init__(self):
        LanguageCheck.__init__(self)

        self.name = "ruby"

        self.checkers.append(RubyClassDeclarationCheck())
        self.checkers.append(RubyFunctionDeclarationCheck())
        self.checkers.append(RubyHeaderCheck())
        self.checkers.append(RubyModuleDeclarationCheck())
        self.checkers.append(RubyRequireCheck())
        self.checkers.append(RubyStrangeFunctionNamesCheck())
