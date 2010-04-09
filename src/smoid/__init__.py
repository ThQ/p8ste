import sys

import smoid.languages.imports
import smoid.languages.namespace
import smoid.languages.package
import smoid.languages.perl
import smoid.languages.php
import smoid.languages.python
import smoid.languages.ruby
import smoid.languages.shebang
import smoid.languages.xml


class GrandChecker:
    def __init__ (self):
        self.languages = {}
        self.checkers = []
        self.checkers.append(smoid.languages.imports.ImportCheck())
        self.checkers.append(smoid.languages.namespace.NamespaceCheck())
        self.checkers.append(smoid.languages.package.PackageCheck())
        self.checkers.extend(smoid.languages.perl.PerlCheckCollection())
        self.checkers.extend(smoid.languages.php.PhpCheckCollection())
        self.checkers.extend(smoid.languages.python.PythonCheck())
        self.checkers.extend(smoid.languages.ruby.RubyCheckCollection())
        self.checkers.append(smoid.languages.shebang.ShebangCheck())
        self.checkers.extend(smoid.languages.xml.XmlCheck())
        self.verbose = False

    def find_out_language_of_file (self, file_path):
        lang = ""
        hfile = open(file_path)
        if hfile:
            file_content = hfile.read()
            lang = self.find_out_language (file_content)
            hfile.close()
        return lang

    def find_out_language(self, str):
        self.languages = {}
        check_no = 0

        for checker in self.checkers:
            if self.verbose:
               check_no += 1
               print "#" + repr(check_no) + ".",
               checker.check_verbose(str)
            else:
               checker.check(str)

            for language_name in checker.languages:
                language = checker.languages[language_name]
                if not self.languages.has_key(language_name):
                    self.languages[language_name] = {"name": language_name, "probability": language.probability}
                else:
                    self.languages[language_name]["probability"] += language.probability

        results = self.languages.values()
        results = sorted(results, GrandChecker.sort_language)

        if self.verbose:
            print "\nProbabilities..."
            for language in results:
                if language["probability"] > 0:
                    print "[", language["name"], "] =", language["probability"]

        language = ""
        if len(results) > 1 and results[0]["probability"] > 0:
            language = results[0]["name"]

        return language

    @staticmethod
    def sort_language (checker1, checker2):
        if checker1["probability"] > checker2["probability"]:
            return -1
        elif checker1["probability"] == checker2["probability"]:
            return 0
        else:
            return 1
