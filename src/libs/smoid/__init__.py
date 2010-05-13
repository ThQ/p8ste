import sys


import smoid.languages.ada
import smoid.languages.klass
import smoid.languages.html
import smoid.languages.imports
import smoid.languages.namespace
import smoid.languages.package
import smoid.languages.perl
import smoid.languages.php
import smoid.languages.python
import smoid.languages.python_console
import smoid.languages.ruby
import smoid.languages.sh
import smoid.languages.shebang
import smoid.languages.sql
import smoid.languages.xml


class GrandChecker:
    def __init__ (self):
        self.languages = {}
        self.checkers = []
        self.checkers.extend(smoid.languages.ada.AdaCheckCollection())
        self.checkers.append(smoid.languages.klass.KlassCheck())
        self.checkers.extend(smoid.languages.html.HtmlCheckCollection())
        self.checkers.append(smoid.languages.imports.ImportCheck())
        self.checkers.append(smoid.languages.namespace.NamespaceCheck())
        self.checkers.append(smoid.languages.package.PackageCheck())
        self.checkers.extend(smoid.languages.perl.PerlCheckCollection())
        self.checkers.extend(smoid.languages.php.PhpCheckCollection())
        self.checkers.extend(smoid.languages.python.PythonCheck())
        self.checkers.extend(smoid.languages.python_console.PythonConsoleCheck())
        self.checkers.extend(smoid.languages.ruby.RubyCheckCollection())
        self.checkers.extend(smoid.languages.sh.ShCollection())
        self.checkers.append(smoid.languages.shebang.ShebangCheck())
        self.checkers.extend(smoid.languages.sql.SqlCheckCollection())
        self.checkers.extend(smoid.languages.xml.XmlCheck())
        self.verbose = False
        self.max_checker_name_length = 30

    def check (self, content):
        check_no = 0

        check_no_filled_width = len(str(len(self.checkers)))

        for checker in self.checkers:

            if self.verbose:
               check_no += 1
               display_name = ("<" + checker.name + ">...").ljust(self.max_checker_name_length)
               print "#" + str(check_no).zfill(check_no_filled_width) + ".",
               print "Checking " + display_name,

            checker.check(content)

            for language_name in checker.languages:
                language = checker.languages[language_name]
                if not self.languages.has_key(language_name):
                    self.languages[language_name] = {"name": language_name, "probability": language.probability}
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
