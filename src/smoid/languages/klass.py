import re


from smoid.languages import Check, CheckCollection


class KlassCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Class"
        self.example = "public class GreatClassRight : DadClass"
        self.add_language("java")
        self.add_language("csharp")

        self.java_modifiers = ["abstract", "public", "private"]
        self.csharp_modifiers = ["abstract", "public", "private", "protected", "internal"]

        class_modifiers = ["abstract", "public", "private", "protected", "internal"]

        res_modifiers = ""
        for modifier in class_modifiers:
            if res_modifiers != "":
                res_modifiers += "|"
            res_modifiers += "(?:" + modifier + "\s+)"
        res_modifiers = "((?:" + res_modifiers + ")*)"

        res_class_name = "[a-zA-Z0-9_][a-zA-Z0-9_-]*"
        res_class = "(?:\n|\r|;|^)\s*" + res_modifiers + "class " + res_class_name + ""

        self.re_class = re.compile(res_class)

    def check (self, content):
        self.reset()
        matches = self.re_class.findall(content)

        for match in matches:
            self.incr_language_probability("java", 20)
            self.incr_language_probability("csharp", 20)

            modifiers = match.split(" ")
            for modifier in modifiers:
                if modifier.strip() in self.java_modifiers:
                    self.incr_language_probability("java", 10)

                if modifier.strip() in self.csharp_modifiers:
                    self.incr_language_probability("csharp", 10)
