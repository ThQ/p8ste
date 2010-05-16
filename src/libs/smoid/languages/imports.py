import re


from smoid.languages import Check, CheckCollection


class ImportCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Import"
        self.example = "import org.apache.hadoop.conf.Configuration;"
        self.add_language("java")
        self.add_language("python")
        self.add_language("scala")
        res_package = "\s*import\s+([a-zA-Z_.]+)\s*(?:\n|\r|;)"
        self.re_package = re.compile(res_package)

    def check (self, content):
        self.reset()
        matches = self.re_package.findall(content)

        for match in matches:
            self.incr_probability(10)
            if match[0:5] == "java.":
                self.incr_language_probability("java", 20)
                self.incr_language_probability("scala", 20)
