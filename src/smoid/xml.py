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


import check


class XmlDeclarationCheck (check.Check):
    def __init__ (self):
        check.Check.__init__(self)
        self.name = "XML declaration : <?xml etc."

    def _test(self):
        result = False
        if self.is_re_found("^<\?xml\s+") :
            self.probability = 40
            result = True
        return result


class XmlCheck (check.LanguageCheck):
    def __init__(self):
        check.LanguageCheck.__init__(self)

        self.name="ruby"

        self.checkers.append(XmlDeclarationCheck())
