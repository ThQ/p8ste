from languages import Check, CheckCollection


class PhpChildClassDeclarationCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "PhpClassDeclaration"
        self.example = "class MyClassIsColl extends Dad {"

        self.add_language("php")
        re_id = "[a-zA-Z_][a-zA-Z0-9_]*"
        self.add_multiple_matches("class\s+" + re_id + "\s+(implements)|(extends)\s+" + re_id + "\s*{", 60)


class PhpClosingTagCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "PhpClosingTag"
        self.example = "?>"

        self.add_language("php")
        self.add_one_time_match("(^|\n|\r)\?>", 80)


class PhpInstanceMemberCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "PhpInstanceMember"
        self.example = "$my_var->is_cool"

        self.add_language("php")
        self.add_multiple_matches("\$[a-zA-Z_][a-zA-Z0-9]*->[a-zA-Z_][a-zA-Z0-9]*", 20)


class PhpGetPostVariablesCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "PhpGetPostVariables"
        self.example = "$_GET";
        self.add_language("php")

        self.add_multiple_matches("\$_(GET)|(POST)", 20)


class PhpOpeningTagCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "PhpOpeningTag"
        self.example = "<?php"
        self.add_language("php")
        self.add_one_time_match("\<\?php\\s|\n|\r", 80)


class PhpCheckCollection (CheckCollection):
    def __init__ (self):

        self.append(PhpChildClassDeclarationCheck())
        self.append(PhpClosingTagCheck())
        self.append(PhpGetPostVariablesCheck())
        self.append(PhpOpeningTagCheck())
