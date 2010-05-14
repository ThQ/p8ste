import re

from smoid.languages import Check, CheckCollection


class AdaWithCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Ada:With"
        self.example = "private with Ada.Strings.Unbounded"

        self.add_language("ada")

        res_sol = "(?:\r|\n|^|;)"
        res_scope = "(?:(?:private|limited)\s+)?"
        res_id = "([a-zA-Z_][a-zA-Z0-9_.]*)"
        res_with = res_sol + "\s*" + res_scope + "\s*with\s+" + res_id + "\s*;"

        self.re_with = re.compile(res_with)

    def check (self, content):
        for match in self.re_with.finditer(content):
            self.incr_language_probability("ada", 30)

            if match.group(1).startswith("Ada.") or match.group(1).startswith("GNAT."):
                self.incr_language_probability("ada", 50)


class AdaRaiseCheck (Check):
    def __init__ (self):

        Check.__init__(self)

        self.name = "Ada:Raise"
        self.example = "raise Name_Absent;"

        self.add_language("ada")

        self.add_multiple_matches("(?:^|\r|\n|;)\s*raise\s*([a-zA-Z0-9_'.]+)\s*;", 50)


class AdaRaiseExceptionCheck (Check):
    def __init__ (self):

        Check.__init__(self)

        self.name = "Ada:RaiseException"
        self.example = "Raise_Exception (Valve_Failure'Identity, \"Failure while closing\");"

        self.add_language("ada")

        self.add_multiple_matches("(?:^|\r|\n|;)\s*Raise_Exception\s*\(([a-zA-Z0-9_'.]+)\s*,", 50)


class AdaCheckCollection (CheckCollection):
    def __init__ (self):

        self.append(AdaRaiseCheck())
        self.append(AdaRaiseExceptionCheck())
        self.append(AdaWithCheck())
