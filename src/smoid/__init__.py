import sys

import languages.perl
import languages.php
import languages.python
import languages.ruby
import languages.xml


class GrandChecker:
    def __init__ (self):
        self.languages = {}
        self.checkers = []
        self.checkers.extend(languages.perl.PerlCheckCollection())
        self.checkers.extend(languages.php.PhpCheckCollection())
        self.checkers.extend(languages.python.PythonCheck())
        self.checkers.extend(languages.ruby.RubyCheckCollection())
        self.checkers.extend(languages.xml.XmlCheck())
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
            probability = 0
            if self.verbose:
               check_no += 1
               print "#" + repr(check_no) + ".",
               checker.check_verbose(str)
            else:
               checker.check(str)
            probability = checker.probability

            for language in checker.languages:
                if not self.languages.has_key(language):
                    self.languages[language] = {"name": language, "probability": probability}
                else:
                    self.languages[language]["probability"] += probability

        results = self.languages.values()
        results = sorted(results, GrandChecker.sort_language)
        if self.verbose:
            print "\nProbabilities..."
            for language in results:
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
