# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It  is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.

import sys

import languages.perl
import languages.php
#import languages.python
#import languages.ruby
#import languages.xml


class GrandChecker:
    def __init__ (self):
        self.languages = {}
        self.checkers = []
        self.checkers.extend(languages.perl.PerlCheckCollection())
        self.checkers.extend(languages.php.PhpCheckCollection())
        #self.checkers.append(languages.python.PythonCheck())
        #self.checkers.append(languages.ruby.RubyCheck())
        #self.checkers.append(languages.xml.XmlCheck())
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
        for checker in self.checkers:
            probability = 0
            if self.verbose:
               probability =  checker.check_verbose(str)
            else:
               probability = checker.check(str)

            if probability != 0:
                for language in checker.languages:
                    if not self.languages.has_key(language):
                        self.languages[language] = probability
                    else:
                        self.languages[language] = probability

        self.checkers = sorted(self.checkers, GrandChecker.sort_language)

        if self.verbose:
            print "\nProbabilities..."
            for language_probability in self.languages:
                print "[] =", language_probability

        language = ""
        if len(self.checkers) > 1 and self.checkers[0].probability > 0:
            language = self.checkers[0].name
        return language

    @staticmethod
    def sort_language (checker1, checker2):
        if checker1.probability > checker2.probability:
            return -1
        elif checker1.probability == checker2.probability:
            return 0
        else:
            return 1
