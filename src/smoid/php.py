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

import check


class PhpChildClassDeclarationCheck (check.Check):
    def __init__ (self):
        check.Check.__init__ (self)
        self.name = "Class declaration (class * implements *)"

    def _test(self):
        result = False
        if self.is_re_found("class\s+[a-zA-Z_][a-zA-Z0-9_]*\s+implements\s+[a-zA-Z_][a-zA-Z0-9_]*\s*{"):
            self.probability = 60
            result = True
        return result


class PhpHeaderCheck (check.Check):
    def __init__ (self):
        check.Check.__init__ (self)
        self.name = "Header (#!.../php)"

    def _test(self):
        result = False
        if self.is_re_matched("#!/(.+)php(\n|$)"):
            self.probability = 100
            result = True
        return result


class PhpInstanceMemberCheck (check.Check):
    name = "PhpInstanceMember"

    def _test(self):
        result = False
        if self.is_re_matched("\$[a-zA-Z_][a-zA-Z0-9]*->"):
            result = True
        return result


class PhpGetPostVariablesCheck (check.Check):
    def __init__ (self):
        check.Check.__init__ (self)
        self.name = "$_GET / $_POST variables"

    def _test(self):
        result = False
        if self.is_re_found("\$_(GET)|(POST)"):
            self.probability = 40
            result = True
        return result


class PhpOpeningTagCheck (check.Check):

    def __init__ (self):
        check.Check.__init__ (self)
        self.name = "Opening tag (<?php)"

    def _test(self):
        result = False
        if self.is_re_matched("\<\?php\\s|\n|\r"):
            result = True
            self.probability = 50
        return result


class PhpCheck (check.LanguageCheck):
    def __init__ (self):
        check.LanguageCheck.__init__(self)
        self.name = "php"
        self.checkers.append (PhpHeaderCheck())
        self.checkers.append (PhpOpeningTagCheck())
        self.checkers.append (PhpGetPostVariablesCheck())
        self.checkers.append (PhpChildClassDeclarationCheck())
