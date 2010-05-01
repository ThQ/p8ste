from smoid.languages import Check, CheckCollection


class RubyClassDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "RubyClassDeclaration"
        self.example = "CoolClass < CoolClassDad"

        self.add_language("ruby")
        re_class = "[a-zA-Z_][a-zA-Z_0-9]+"
        self.add_multiple_matches("(^|\r|\n)\s*class\s+" + re_class + "\s*<<?\s*" + re_class + "\s*(\r|\n|$)", 30)


class RubyFunctionDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "RubyFunctiondeclaration"
        self.example = "def do_it!"
        self.add_language("ruby")
        self.add_multiple_matches("(^|\r|\n)\s*def\s+(self\.)?[a-zA-Z_][a-zA-Z_0-9]*(!|\?)?", 20)


class RubyModuleDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "RubyModuleDeclaration"
        self.example = "module CoolModule"
        self.add_language("ruby")
        self.add_multiple_matches("(^|\r|\n)\s*module\s+[a-zA-Z_][a-zA-Z_0-9]*", 20)


class RubyRequireCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "RubyRequire"
        self.example = "require 'dude.rb'"
        self.add_language("ruby")
        self.add_multiple_matches("(^|\n|\r)\s*require\s+'[^']+'\s*(\r|\n|$)", 40)


class RubyStrangeFunctionNamesCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "RubyStrangeFunctionNames"
        self.example = ".do_it!"
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
