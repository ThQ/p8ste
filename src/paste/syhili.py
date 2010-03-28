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

import cgi
import pygments.formatter
from pygments.token import Token

class HtmlFormatter (pygments.formatter.Formatter):

    def _format_value(self, value, css_class):
        result = ""
        if value.find("\n") != -1:
            lines = value.splitlines()
            for line in lines:
                result += "<span class=\"" + css_class + "\">" + cgi.escape(line) + "</span>\n"
        else:
            result = "<span class=\"" + css_class + "\">" + cgi.escape(value) + "</span>"
        return result

    def format (self, tokens, outfile):
        result = ""

        for token in tokens:
            print token
            if token[0] in Token.Keyword:
                result += self._format_value(token[1], "kw")

            elif token[0] in Token.Comment or token[0] in Token.String.Doc:
                result += self._format_value(token[1], "cmt")

            elif token[0] in Token.Name.Builtin:
                result += self._format_value(token[1], "bui")

            elif token[0] in Token.Literal.String:
                result += self._format_value(token[1], "str")

            else:
                result += cgi.escape(token[1])

        outfile.write(result)
