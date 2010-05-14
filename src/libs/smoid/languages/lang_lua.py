from smoid.languages import Check, CheckCollection, CheckLanguage


class LuaFunctionDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Lua:FunctionDeclaration"
        self.example = "sub do_as_i_say {"
        self.add_language("lua")

        re_var = "[a-zA-Z0-9_.:]+"
        re_func = "(?:\n|\r|=)\s*(local\s*)?function(\s*" + re_var + ")?\s*\((" + re_var + "(?:\s*,\s*" + re_var + "|...)*)?\)(?:\r|\n)"

        self.add_multiple_matches(re_func, 50)


class LuaCheckCollection (CheckCollection):

    def __init__(self):
        self.append(LuaFunctionDeclarationCheck())
