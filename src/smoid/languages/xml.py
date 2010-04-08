from smoid.languages import Check, CheckCollection


class XmlDeclarationCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "XMLDeclaration"
        self.example = "<?xml"
        self.add_language("xml")
        self.add_one_time_match("^<\?xml\s+", 100)


class XmlCheck (CheckCollection):
    def __init__(self):
        self.name = "xml"

        self.append(XmlDeclarationCheck())
