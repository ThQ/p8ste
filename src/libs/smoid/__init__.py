import sys


import smoid.languages.begin
import smoid.languages.exception
import smoid.languages.klass
import smoid.languages.imports
import smoid.languages.lang_ada
import smoid.languages.lang_c
import smoid.languages.lang_html
import smoid.languages.lang_lua
import smoid.languages.lang_perl
import smoid.languages.lang_php
import smoid.languages.lang_python
import smoid.languages.lang_python_console
import smoid.languages.lang_ruby
import smoid.languages.lang_sh
import smoid.languages.lang_sql
import smoid.languages.lang_xml
import smoid.languages.namespace
import smoid.languages.package
import smoid.languages.shebang
import smoid.languages.whyle


class GrandChecker:
    def __init__ (self):
        self.languages = {}
        self.checkers = []

        self.checkers.extend(smoid.languages.lang_ada.AdaCheckCollection())
        self.checkers.extend(smoid.languages.lang_c.CCheckCollection())
        self.checkers.extend(smoid.languages.lang_html.HtmlCheckCollection())
        self.checkers.extend(smoid.languages.lang_lua.LuaCheckCollection())
        self.checkers.extend(smoid.languages.lang_perl.PerlCheckCollection())
        self.checkers.extend(smoid.languages.lang_php.PhpCheckCollection())
        self.checkers.extend(smoid.languages.lang_python.PythonCheck())
        self.checkers.extend(smoid.languages.lang_python_console.PythonConsoleCheck())
        self.checkers.extend(smoid.languages.lang_ruby.RubyCheckCollection())
        self.checkers.extend(smoid.languages.lang_sh.ShCollection())
        self.checkers.extend(smoid.languages.lang_sql.SqlCheckCollection())
        self.checkers.extend(smoid.languages.lang_xml.XmlCheck())

        self.checkers.append(smoid.languages.begin.BeginCheck())
        self.checkers.extend(smoid.languages.exception.ExceptionCheckCollection())
        self.checkers.append(smoid.languages.klass.KlassCheck())
        self.checkers.append(smoid.languages.imports.ImportCheck())
        self.checkers.append(smoid.languages.namespace.NamespaceCheck())
        self.checkers.append(smoid.languages.package.PackageCheck())
        self.checkers.append(smoid.languages.shebang.ShebangCheck())
        self.checkers.append(smoid.languages.whyle.WhileCheck())

        self.verbose = False
        self.max_checker_name_length = 30

    def check (self, content):
        types = [
            smoid.languages.Check.kTYPE_FINAL,
            smoid.languages.Check.kTYPE_MACRO,
            smoid.languages.Check.kTYPE_MICRO
        ]

        for t in types:
            self.check_type (t, content)

    def check_type (self, t,  content):

        for checker in self.checkers:
            if checker.type == t:
                if self.verbose:
                   display_name = ("<" + checker.name + ">...").ljust(self.max_checker_name_length)
                   print "[" + self.get_check_type_name(checker.type) + "]",
                   print "Checking " + display_name,

                checker.check(content)

                for language_name in checker.languages:
                    language = checker.languages[language_name]
                    if not language_name in self.languages.has_key:
                        lang = {}
                        lang["name"] = language_name
                        lang["probability"] = language.probability
                        self.languages[language_name] = lang
                    else:
                        self.languages[language_name]["probability"] += language.probability

                did_languages_passed = False
                languages = ""
                if len(checker.languages) > 0:
                    for language_name in checker.languages:
                        prob = checker.languages[language_name].probability
                        if prob > 0:
                            languages += language_name + " +" + str(prob) + ", "
                            did_languages_passed = True

                if self.verbose:
                    if did_languages_passed:
                        print "[" + languages[:-2] + "]"
                    else:
                        print "-"

    def get_check_type_name (self, t):
        name = ""
        if t == smoid.languages.Check.kTYPE_FINAL:
            name = "FINAL"
        elif t == smoid.languages.Check.kTYPE_MACRO:
            name = "MACRO"
        elif t == smoid.languages.Check.kTYPE_MICRO:
            name = "MICRO"
        else:
            name = "UNKNO"
        return name

    def find_out_language_of_file (self, file_path):
        lang = ""
        hfile = open(file_path)
        if hfile:
            file_content = hfile.read()
            lang = self.find_out_language (file_content)
            hfile.close()
        return lang

    def find_out_language(self, content):
        self.languages = {}
        self.check(content)
        results = self.languages.values()
        results = sorted(results, GrandChecker.sort_language)

        if self.verbose:
            print "\nProbabilities..."
            for language in results:
                if language["probability"] > 0:
                    print "[", language["name"], "] =", language["probability"]

        language = ""
        if len(results) > 0:
            language = results[0]["name"]

        # Top 2 languages have the same probabilities, can't decide
        if len(results) > 1 and results[0]["probability"] == results[1]["probability"]:
            language = ""
        return language

    @staticmethod
    def sort_language (checker1, checker2):
        if checker1["probability"] > checker2["probability"]:
            return -1
        elif checker1["probability"] == checker2["probability"]:
            return 0
        else:
            return 1
