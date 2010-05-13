import re


from smoid.languages import Check, CheckCollection


class PackageCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Package"
        self.example = "package com::my::dear"
        self.add_language("ada")
        self.add_language("java")
        self.add_language("perl")
        res_package = "(?:^|\n|\r|;)\s*package(?:\s*body)?\s*([a-zA-Z_0-9:.]+)\s*($|\n|\r|;|is)"
        self.re_package = re.compile(res_package)

    def check (self, content):
        self.reset()
        matches = self.re_package.search(content)

        for match in self.re_package.finditer(content):

            if match.group(2) == "is":
                self.incr_language_probability("ada", 30)
            else:
                if match.group(1).find(".") != -1:
                    self.incr_language_probability("java", 10)

                elif match.group(1).find("::") != -1:
                    self.incr_language_probability("perl", 10)

                else:
                    self.incr_language_probability("java", 10)
                    self.incr_language_probability("perl", 10)

