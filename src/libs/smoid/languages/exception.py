import re

from smoid.languages import Check, CheckCollection


class ExceptionCatchCheck (Check):
    def __init__ (self):
        Check.__init__ (self)

        self.name = "Exception/Catch"
        self.example = "catch (std::exception &e) {"
        self.type = Check.kTYPE_MICRO

        res_class = "[a-zA-Z0-9_][a-zA-Z0-9_:.]*"
        res_var = "[a-zA-Z0-9_]+"

        self.add_language("c++")
        res_catch = "(?:\n|^|;|})\s*catch\s*\(\s*(?:" + res_class + "[\s&]+(" + res_var + ")?)|(?:\.\.\.)\s*\)[\s\n\r]*{"
        self.add_multiple_matches(res_catch, 20)

class ExceptionTryCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Exception/Try"
        self.example = "try {"
        self.type = Check.kTYPE_MICRO

        self.add_language("c++")
        self.add_language("c#")

        self.add_multiple_matches("(?:\n|^|;)\s*try[\s\n\r]*{", 20)


class ExceptionCheckCollection (CheckCollection):
    def __init__ (self):

        self.append(ExceptionCatchCheck())
        self.append(ExceptionTryCheck())
