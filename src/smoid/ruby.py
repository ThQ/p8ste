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

class RubyTestHeader(Test):
    name = "RubyTestHeader"

    def _test(self):
        self.confidence = 0
        result = False
        if self.is_re_matched("^#!/(.+)ruby(\n|$)") :
            result = True
        return result


class RubyTestChain (TestChain):
    def __init__(self):
        self.tests.append(RubyTestHeader())

