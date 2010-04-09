import re


from smoid.languages import Check, CheckCollection


class PackageCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Package"
        self.example = "package com::my::dear"

        res_package = "(?:^|\n|\r|;)\s*package\s*([a-zA-Z_][a-zA-Z_0-9:.]*)\s*(?:$|\n|\r|;)"
        self.re_package = re.compile(res_package)

    def check (self, content):
        self.probability = 0
        matches = self.re_package.findall(content)
        for match in matches:
            if match.find(".") != -1:
                self.set_languages(["java"])
                self.probability += 10
            elif match.find("::") != -1:
                self.set_languages(["perl"])
                self.probability += 10
