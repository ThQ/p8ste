# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.

languages = []

def get_by_tag(tag):
    result = None
    for lang in languages:
        if tag in lang.tags:
            result = lang
            break
    return result

    result = False
    for lang in languages:
        if tag in lang.tags:
            result = True
            break
    return result


class Language:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.url = ""


class Ada (Language):
    def __init__(self):
        self.name = "Ada"
        self.tags = ["ada"]
        self.url = "http://en.wikipedia.org/wiki/Ada_%28programming_language%29"
languages.append(Ada())


class Bash (Language):
    def __init__(self):
        self.name = "Bash"
        self.tags = ["bash"]
        self.url = "http://www.gnu.org/software/bash/"
languages.append(Bash())


class C (Language):
    def __init__(self):
        self.name = "C"
        self.tags = ["c"]
        self.url = "http://en.wikipedia.org/wiki/C_%28programming_language%29"
languages.append(C())


class CPlusPlus (Language):
    def __init__(self):
        self.name = "C++"
        self.tags = ["c++", "cpp"]
        self.url = "http://en.wikipedia.org/wiki/C++"
languages.append(CPlusPlus())


class CSharp (Language):
    def __init__(self):
        self.name = "C#"
        self.tags = ["c#", "cs", "csharp"]
        self.url = "http://msdn.microsoft.com/en-us/vcsharp/aa336809.aspx"
languages.append(CSharp())


class Haskell (Language):
    def __init__(self):
        self.name = "Haskell"
        self.tags = ["haskell"]
        self.url = "http://www.haskell.org"
languages.append(Haskell())


class Html (Language):
    def __init__(self):
        self.name = "HTML"
        self.tags = ["html"]
        self.url = "http://www.w3.org/TR/html/"
languages.append(Html())


class Java (Language):
    def __init__(self):
        self.name = "Java"
        self.tags = ["java"]
        self.url = "http://java.sun.com/"
languages.append(Java())


class Javascript (Language):
    def __init__(self):
        self.name = "Javascript"
        self.tags = ["javascript"]
        self.url = "http://en.wikipedia.org/wiki/JavaScript"
languages.append(Javascript())


class Lua (Language):
    def __init__(self):
        self.name = "Lua"
        self.tags = ["lua"]
        self.url = "http://www.lua.org/"
languages.append(Lua())


class Perl (Language):
    def __init__(self):
        self.name = "Perl"
        self.tags = ["perl"]
        self.url = "http://www.perl.org"
languages.append(Perl())


class Php (Language):
    def __init__(self):
        self.name = "PHP"
        self.tags = ["php"]
        self.url = "http://www.php.net"
languages.append(Php())


class Python (Language):
    def __init__(self):
        self.name = "Python"
        self.tags = ["python"]
        self.url = "http://www.python.org"
languages.append(Python())


class Ruby (Language):
    def __init__(self):
        self.name = "Ruby"
        self.tags = ["ruby"]
        self.url = "http://www.ruby-lang.org"
languages.append(Ruby())


class Sql (Language):
    def __init__(self):
        self.name = "SQL"
        self.tags = ["sql"]
        self.url = "http://en.wikipedia.org/wiki/SQL"
languages.append(Sql())

