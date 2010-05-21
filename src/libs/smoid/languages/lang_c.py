import re

from smoid.languages import Check, CheckCollection



class CIncludeCheck (Check):
    def __init__ (self):

        Check.__init__(self)

        self.name = "C:Import"
        self.example = "#import <sys/file.h>"

        self.add_language("c")
        self.add_language("c++")

        self.c_std_includes = [
            "assert.h",
            "complex.h",
            "ctype.h",
            "errno.h",
            "fenv.h",
            "float.h",
            "inttypes.h",
            "iso646.h",
            "limits.h"
            "locale.h",
            "math.h",
            "setjmp.h",
            "signal.h",
            "stdarg.h",
            "stdbool.h"
            "stddef.h",
            "stdint.h",
            "stdio.h",
            "stdlib.h",
            "string.h",
            "tgmath.h",
            "time.h",
            "wchar.h",
            "wctype.h"
        ]

        self.cpp_std_includes = [
            "ios",
            "iostream",
            "iomanip",
            "fstream",
            "sstream",
            "vector",
            "deque",
            "list",
            "map",
            "set",
            "stack",
            "queue",
            "bitset",
            "algorithm",
            "memory",
            "functional",
            "iterator",
            "cassert",
            "cctype",
            "cerrno",
            "climits",
            "clocale",
            "cmath",
            "csetjmp",
            "csignal",
            "cstdarg",
            "cstddef",
            "cstdio",
            "cstdint",
            "cstdlib",
            "cstring",
            "ctime"
            "cwchar",
            "cwctype"
        ]

        res_import = """#\s*include\s+(?:"|<|')(.*?)(?:"|<|')(?:\n|\r)"""
        self.re_import = re.compile(res_import)

    def check (self, content):
        self.reset()

        for match in self.re_import.finditer(content):
            self.incr_language_probability("c", 10)
            self.incr_language_probability("c++", 10)

            inc = match.group(1)

            if inc in self.c_std_includes:
                self.incr_language_probability("c", 40)
                self.incr_language_probability("c++", 40)

            elif inc in self.cpp_std_includes:
                self.incr_language_probability("c++", 40)

            elif inc.endswith("hpp"):
                self.incr_language_probability("c++", 30)

            elif inc.endswith("h"):
                self.incr_language_probability("c", 30)
                self.incr_language_probability("c++", 30)


class CCheckCollection (CheckCollection):
    def __init__ (self):

        self.append(CIncludeCheck())
