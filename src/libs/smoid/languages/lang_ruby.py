import re

from smoid.languages import Check, CheckCollection


class RubyClassDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Ruby:Class/Declaration"
        self.example = "CoolClass < CoolClassDad"

        self.add_language("ruby")
        re_class = "[a-zA-Z_][a-zA-Z_0-9]+"
        self.add_multiple_matches("(^|\r|\n)\s*class\s+" + re_class + "\s*<<?\s*" + re_class + "\s*(\r|\n|$)", 30)


class RubyFunctionDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Ruby:Function/Declaration"
        self.example = "def do_it!"
        self.add_language("ruby")

        res_sol = "(?:^|\r|\n)"
        res_name = "(?:self\.)?[a-zA-Z_][a-zA-Z0-9_]*(?:!|\?)?"
        res_arg = "(?:&|\*)?\s*[a-zA-Z0-9_]+"
        res_args = "(?:\(\s*(" + res_arg + "(?:\s*,\s*" + res_arg + ")*)?\s*\))?"
        res_eol = "\s*(?:\r|\n)"

        res_func = res_sol + "\s*"
        res_func += "def\s+"
        res_func += "(" + res_name + ")\s*"
        res_func += res_args
        res_func += res_eol

        self.re_func = re.compile(res_func)

        self.special_methods = [
            "initialize",
            "inspect",
            "method_missing",
            "respond_to?",
            "to_a",
            "to_enum",
            "to_s"
        ]

    def check (self, content):
        self.reset()

        for match in self.re_func.finditer(content):
            func_name = match.group(1)
            self.incr_language_probability("ruby", 20)
            if func_name in self.special_methods:
                self.incr_language_probability("ruby", 20)

class RubyModuleDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Ruby:Module/Declaration"
        self.example = "module CoolModule"
        self.add_language("ruby")
        self.add_multiple_matches("(^|\r|\n)\s*module\s+[a-zA-Z_][a-zA-Z_0-9]*", 20)


class RubyRequireCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Ruby:Require"
        self.example = "require 'dude.rb'"
        self.add_language("ruby")
        self.add_multiple_matches("(^|\n|\r)\s*require\s+'[^']+'\s*(\r|\n|$)", 40)


class RubyStrangeFunctionNamesCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Ruby:StrangeFunctionNames"
        self.example = ".do_it!"
        self.type = Check.kTYPE_MICRO
        self.add_language("ruby")
        self.add_multiple_matches("\.[a-zA-Z_][a-zA-Z_0-9](\?|!)", 20)


class RubyCheckCollection (CheckCollection):
    def __init__(self):

        self.name = "ruby"

        self.append(RubyClassDeclarationCheck())
        self.append(RubyFunctionDeclarationCheck())
        self.append(RubyModuleDeclarationCheck())
        self.append(RubyRequireCheck())
        self.append(RubyStrangeFunctionNamesCheck())
