from languages import Check, CheckCollection


class ShebangCheck (Check):

    def __init__ (self):
        Check.__init__ (self)
        self.name = "Shebang"
        self.example = "#!/usr/bin/python"
        self.shebang_languages = ["php", "python", "perl", "ruby"]

    def check (self, content):
        content_len = len(content)
        self.probability = 0
        self.langauges = []

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

            if bin in self.shebang_languages:
                self.languages = [bin]
                self.probability = 100

