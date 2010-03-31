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


class PerlPackageCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Package"
        self.example = "package com::my::dear;"

        re_ns = "[a-zA-Z_][a-zA-Z_0-9]*"
        re_full_ns = re_ns + "(?:\s*::\s*" + re_ns + ")*"

        self.add_multiple_matches("(?:^|\n|\r|;)\s*package\s*(" + re_full_ns + ")\s*(?:$|\n|\r|;)", 10)

class PerlShebangCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Shebang"
        self.example = "#!/usr/bin/env perl"

        self.add_one_time_match("^#!/(.+)perl( .*?)?(\n|$)", 60)

class PerlSubroutineCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Subroutine"
        self.example = "sub do_as_i_say {"

        self.add_multiple_matches("(?:^|\n|\r|;)\s*sub\s+([a-zA-Z_][a-zA-Z_0-8]*)\s*{", 10)

class PerlUseCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Use"
        self.example = "use File::Spec;"

        re_ns = "[a-zA-Z_][a-zA-Z_0-9]*"
        re_full_ns = re_ns + "(?:\s*::\s*" + re_ns + ")*"

        self.add_multiple_matches("(?:^|\n|\r|;)\s*use\s*(" + re_full_ns + ")\s*(?:$|\n|\r|;)", 10)


class PerlCheck (LanguageCheck):
    def __init__(self):
        LanguageCheck.__init__(self)

        self.name = "perl"

        self.checkers.append(PerlPackageCheck())
        self.checkers.append(PerlShebangCheck())
        self.checkers.append(PerlSubroutineCheck())
        self.checkers.append(PerlUseCheck())

