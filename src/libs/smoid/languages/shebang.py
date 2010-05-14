from smoid.languages import Check, CheckCollection


class ShebangCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Shebang"
        self.example = "#!/usr/bin/python"
        self.type = Check.kTYPE_FINAL
        self.add_language("perl")
        self.add_language("php")
        self.add_language("python")
        self.add_language("ruby")

    def check (self, content):
        self.reset()
        content_len = len(content)

        if content_len > 2 and content[0:2] == "#!":
            bin_path = ""
            eol_pos = 0
            i = 0
            for c in content[2:]:
                if c == "\n" or c == "\r":
                    eol_pos = i
                    break
                bin_path += c
                i += 1
            slash_pos = bin_path.rfind("/")
            bin = content[slash_pos + 3:i + 2]

            if bin in self.languages.keys():
                self.incr_language_probability(bin, 100)
