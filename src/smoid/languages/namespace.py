import re


from smoid.languages import Check, CheckCollection


class NamespaceCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Namespace"
        self.example = "namespace dude.this.rocks {"
        self.add_language("c#")
        self.add_language("c++")
        res_package = "(?:^|\n|\r|;)\s*namespace\s*([a-zA-Z_][a-zA-Z_0-9.]*)\s*(?:$|\n|\r|;)\s*{"
        self.re_package = re.compile(res_package)

    def check (self, content):
        self.reset()
        matches = self.re_package.findall(content)
        for match in matches:
            if match.find(".") != -1:
                self.incr_language_probability("c#", 10)
            else:
                self.incr_language_probability("c++", 10)
