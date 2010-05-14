from smoid.languages import Check, CheckCollection


class LuaFunctionDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Lua:FunctionDeclaration"
        self.example = "function Knot:load(stream)"
        self.add_language("lua")

        res_sol = "(?:\n|\r|=)"
        res_var = "[a-zA-Z0-9_.:]+"
        res_args = "(" + res_var + "(?:\s*,\s*" + res_var + "|...)*)?"
        res_func = res_sol
        res_func += "\s*(local\s*)?"
        res_func += "function(\s*" + res_var + ")?\s*"
        res_func += "\(" + res_args + "\)(?:\r|\n)"

        self.add_multiple_matches(res_func, 50)


class LuaCheckCollection (CheckCollection):

    def __init__(self):
        self.append(LuaFunctionDeclarationCheck())
