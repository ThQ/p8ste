from smoid.languages import Check, CheckCollection


class ShControlFlowCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "ShControlFlow"
        self.example = "if [ -f ./myfile ] ;"

        self.add_language("sh")

        self.add_multiple_matches("(?:^|\r|\n|;)\s*(el)?if\s*\[(?:[^\]]+?)\]\s*(?:;|\r|\n|$)", 20)
        self.add_multiple_matches("(?:^|\r|\n|;)fi(?:;|\r|\n|$)", 10)


class ShCollection (CheckCollection):
    def __init__ (self):

        self.append(ShControlFlowCheck())
