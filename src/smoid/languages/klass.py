import re


from smoid.languages import Check, CheckCollection


class KlassCheck (Check):
    def __init__ (self):
        Check.__init__(self)

        self.name = "Class"
        self.example = "public class GreatClassRight : DadClass"
        self.add_language("csharp")
        self.add_language("java")
        self.add_language("php")
        self.add_language("scala")

        # http://www.javacamp.org/javaI/Modifier.html
        self.java_modifiers = ["abstract", "final", "public", "private", "static", "strictfp"]

        # http://msdn.microsoft.com/en-us/library/0b0thckt%28VS.71%29.aspx
        self.csharp_modifiers = ["abstract", "new", "public", "private", "protected", "internal", "sealed"]

        self.php_modifiers = ["abstract"]

        self.scala_modifiers = ["private", "protected"]

        prefix_modifiers = []
        prefix_modifiers.extend(self.csharp_modifiers)
        prefix_modifiers.extend(self.java_modifiers)
        prefix_modifiers.extend(self.php_modifiers)

        res_modifiers = ""
        for modifier in prefix_modifiers:
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
            self.incr_language_probability("php", 20)

            if match != "":
                modifiers = match.split(" ")
                for modifier in modifiers:
                    modifier = modifier.strip()
                    if modifier in self.java_modifiers:
                        self.incr_language_probability("java", 10)

                    if modifier in self.csharp_modifiers:
                        self.incr_language_probability("csharp", 10)

                    if modifier in self.php_modifiers:
                        self.incr_language_probability("php", 10)

            else:
                self.incr_language_probability("scala", 20)
