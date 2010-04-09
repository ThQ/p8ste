import re


from smoid.languages import Check, CheckCollection


class NamespaceCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Namespace"
        self.example = "namespace dude.this.rocks {"

        res_package = "(?:^|\n|\r|;)\s*namespace\s*([a-zA-Z_][a-zA-Z_0-9.]*)\s*(?:$|\n|\r|;)\s*{"
        self.re_package = re.compile(res_package)

    def check (self, content):
        self.probability = 0
        matches = self.re_package.findall(content)
        for match in matches:
            if match.find(".") != -1:
                self.set_languages(["c#"])
                self.probability += 10
            else:
                self.set_languages(["c#", "c++"])
                self.probability += 10
