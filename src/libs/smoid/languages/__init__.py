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


import re


languages = {}

languages["ada"] = {
    "lexer": "ada",
    "name": "Ada",
    "home_url": "http://en.wikipedia.org/wiki/Ada_%28programming_language%29",
    "u_icon": "images/languages/ada.png"
}

languages["html"] = {
    "lexer": "html",
    "name": "HTML",
    "home_url": "http://en.wikipedia.org/wiki/HTML",
    "u_icon": "images/languages/html.png"
}

languages["java"] = {
    "lexer": "java",
    "name": "Java",
    "home_url": "http://www.java.com",
    "u_icon": "images/languages/java.png"
}

languages["lua"] = {
    "lexer": "lua",
    "name": "Lua",
    "home_url": "http://www.lua.org",
    "u_icon": "images/languages/lua.png"
}

languages["php"] = {
    "lexer": "php",
    "name": "PHP",
    "home_url": "http://php.net",
    "u_icon": "images/languages/php.png"
}

languages["perl"] = {
    "lexer": "perl",
    "name": "Perl",
    "home_url": "http://www.perl.org",
    "u_icon": "images/languages/perl.png"
}

languages["python"] = {
    "lexer": "python",
    "name": "Python",
    "home_url": "http://python.org",
    "u_icon": "images/languages/python.png"
}

languages["python_console"] = {
    "lexer": "pycon",
    "name": "Python Console",
    "home_url": "http://python.org",
    "u_icon": "images/languages/python.png"
}

languages["ruby"] = {
    "lexer": "ruby",
    "name": "Ruby",
    "home_url": "http://www.ruby-lang.org",
    "u_icon": "images/languages/ruby.png"
}

languages["scala"] = {
    "lexer": "scala",
    "name": "Scala",
    "home_url": "http://www.scala-lang.org",
    "u_icon": "images/languages/scala.png"
}

languages["sql"] = {
    "lexer": "sql",
    "name": "SQL",
    "home_url": "http://en.wikipedia.org/wiki/SQL",
    "u_icon": "images/languages/sql.png"
}

languages["sh"] = {
    "lexer": "sh",
    "name": "Shell",
    "home_url": "http://en.wikipedia.org/wiki/Shell_(computing)",
    "u_icon": "images/languages/sh.png"
}

languages["xml"] = {
    "lexer": "xml",
    "name": "XML",
    "home_url": "http://www.w3.org/TR/2006/REC-xml11-20060816/",
    "u_icon": "images/languages/xml.png"
}

class Check:
    kTYPE_FINAL = 1
    kTYPE_MACRO = 2
    kTYPE_MICRO = 3

    def __init__(self):
        self.content = ""
        self.example = ""
        self.languages = {}
        self.multiple_matches = []
        self.name = ""
        self.one_time_matches = []
        self.type = Check.kTYPE_MACRO

    def add_language (self, language_name):
        self.languages[language_name] = CheckLanguage(name=language_name)

    def add_multiple_matches (self, regex, probability):
        self.multiple_matches.append((regex, probability))

    def add_one_time_match (self, regex, probability):
        self.one_time_matches.append((regex, probability))

    def check (self, content):
        self.content = content
        self.reset()
        for match in self.one_time_matches:
            if self.is_re_matched(match[0]):
                for lang in self.languages:
                    self.languages[lang].probability += match[1]

        for match_info in self.multiple_matches:
            all_matched = re.findall(match_info[0], content)
            for matched in all_matched:
                for lang in self.languages:
                    self.languages[lang].probability += match_info[1]

        self._test()

    def incr_language_probability (self, name, prob_diff):
        if name in self.languages:
            self.languages[name].probability += prob_diff

    def incr_probability (self, prob_diff):
        for language_name in self.languages:
            self.languages[language_name].probability += prob_diff

    def is_re_found (self, regex, start_at = 0):
        return re.compile(regex).search(self.content, start_at)

    def is_re_matched (self, regex, start_at = 0):
        return re.compile(regex).match(self.content, start_at)

    def reset (self):
        for language_name in self.languages:
            self.languages[language_name].probability = 0

    def set_languages (self, languages):
        self.languages = languages

    def set_type (self, t):
        self.type = t

    def _test (self):
        pass

class CheckLanguage:
    def __init__ (self, name="", probability=0):
        self.name = name
        self.probability = probability

class CheckCollection (list):
    pass
