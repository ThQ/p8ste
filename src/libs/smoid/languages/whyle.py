

import re

from smoid.languages import Check, CheckCollection


class WhileCheck (Check):
    def __init__ (self):

        Check.__init__(self)

        self.name = "While"
        self.example = "while true do"

        self.add_language("c")
        self.add_language("cpp")
        self.add_language("csharp")
        self.add_language("lua")
        self.add_language("perl")
        self.add_language("php")
        self.add_language("python")
        self.add_language("ruby")

        res_sol = "(?:^|\n|\r|;)"
        res_eol = "(do|:|{)"

        res_while = res_sol + "\s*while(\s+|\(\s*).*?(\))?" + res_eol

        self.re_while = re.compile(res_while)

    def check (self, content):
        self.reset()

        for match in self.re_while.finditer(content):
            eol = match.group(3)

            if eol == "do":
                self.incr_language_probability("lua", 30)
                self.incr_language_probability("ruby", 30)

            elif eol == ":":
                self.incr_language_probability("python", 30)

            elif eol == "{":
                self.incr_language_probability("c", 30)
                self.incr_language_probability("cpp", 30)
                self.incr_language_probability("csharp", 30)
                self.incr_language_probability("perl", 30)
                self.incr_language_probability("php", 30)
