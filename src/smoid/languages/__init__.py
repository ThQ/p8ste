import re

languages = {}

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

languages["ruby"] = {
    "lexer": "ruby",
    "name": "Ruby",
    "home_url": "http://www.ruby-lang.org",
    "u_icon": "images/languages/ruby.png"
}

languages["xml"] = {
    "lexer": "xml",
    "name": "XML",
    "home_url": "http://www.w3.org/TR/2006/REC-xml11-20060816/",
    "u_icon": "images/languages/xml.png"
}


class Check:

    def __init__(self):
        self.content = ""
        self.example = ""
        self.name = ""
        self.probability = 0
        self.one_time_matches = []
        self.multiple_matches = []


    def add_multiple_matches (self, regex, probability):
        self.multiple_matches.append((regex, probability))

    def add_one_time_match (self, regex, probability):
        self.one_time_matches.append((regex, probability))

    def check (self, content):
        self.content = content

        for match in self.one_time_matches:
            if self.is_re_matched(match[0]):
                self.probability += match[1]

        for match_info in self.multiple_matches:
            all_matched = re.findall(match_info[0], content)
            for matched in all_matched:
                self.probability += match_info[1]

        self._test()

    def check_verbose (self, content):
        print " * Checking [", self.name, "]... ",
        result = self.check(content)
        print "+" + str(self.probability)
        return result

    def is_re_found (self, regex, start_at = 0):
        return re.compile(regex).search(self.content, start_at)

    def is_re_matched (self, regex, start_at = 0):
        return re.compile(regex).match(self.content, start_at)

    def _test (self):
        pass

class LanguageCheck:

    def __init__ (self):
        self.name = ""
        self.probability = 0
        self.checkers = []

    def check (self, str):
        for checker in self.checkers:
            checker.check(str)
            self.probability += checker.probability

    def check_verbose (self, str):
        print "Performing language check for ", self.name, "... (", len(self.checkers), " tests )"
        for checker in self.checkers:
            checker.check_verbose(str)
            self.probability += checker.probability
        print "   [ Probably of this string to be", self.name, "= ", self.probability, "]\n"
