from smoid.languages import Check, CheckCollection


class PhpChildClassDeclarationCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Php:ClassDeclaration"
        self.example = "class MyClassIsColl extends Dad {"

        self.add_language("php")
        re_id = "[a-zA-Z_][a-zA-Z0-9_]*"
        self.add_multiple_matches("class\s+" + re_id + "\s+(implements)|(extends)\s+" + re_id + "\s*{", 60)


class PhpClosingTagCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Php:ClosingTag"
        self.example = "?>"

        self.add_language("php")
        self.add_one_time_match("(^|\n|\r)\?>", 80)


class PhpInstanceMemberCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Php:InstanceMember"
        self.example = "$my_var->is_cool"
        self.type = Check.kTYPE_MICRO

        self.add_language("php")
        self.add_multiple_matches("\$[a-zA-Z_][a-zA-Z0-9]*->[a-zA-Z_][a-zA-Z0-9]*", 20)


class PhpGetPostVariablesCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Php:GetPostVariables"
        self.example = "$_GET";
        self.type = Check.kTYPE_MICRO
        self.add_language("php")

        self.add_multiple_matches("\$_(GET)|(POST)", 20)


class PhpOpeningTagCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Php:OpeningTag"
        self.example = "<?php"
        self.add_language("php")
        self.add_one_time_match("\<\?php\\s|\n|\r", 80)


class PhpCheckCollection (CheckCollection):
    def __init__ (self):

        self.append(PhpChildClassDeclarationCheck())
        self.append(PhpClosingTagCheck())
        self.append(PhpInstanceMemberCheck())
        self.append(PhpGetPostVariablesCheck())
        self.append(PhpOpeningTagCheck())
