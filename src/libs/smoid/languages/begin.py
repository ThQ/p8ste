

from smoid.languages import Check, CheckCollection


class BeginCheck (Check):
    def __init__ (self):

        Check.__init__(self)

        self.name = "Begin"
        self.example = "begin"

        self.add_language("ada")
        self.add_language("ruby")

        self.add_multiple_matches("(?:^|\r|\n|;)\s*begin\s*(?:\r|\n)", 10)
