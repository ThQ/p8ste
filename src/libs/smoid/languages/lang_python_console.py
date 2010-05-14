from smoid.languages import Check, CheckCollection


class PythonConsoleLineStartCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "PythonConsole:LineStart"
        self.example = ">>> 1 + 1"
        self.add_language("python_console")
        self.add_multiple_matches("(?:^|\n|\r)>>>", 30)


class PythonConsoleCheck (CheckCollection):
    def __init__(self):
        self.name = "python"

        self.append(PythonConsoleLineStartCheck())
