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

import pygments.lexers
import pygments.formatters

import smoid.languages
import paste
import paste.lang
import paste.model
import paste.util
import paste.web
import settings

class Update (paste.web.RequestHandler):

    def __init__ (self):
        paste.web.RequestHandler.__init__(self)
        self.paste = None
        self.set_module("page.pasties.update.__init__")

    def get (self, paste_slug):
        self.paste = self.get_paste(paste_slug)

        self.content["u_pastes"] = paste.url("pastes/")
        self.content["u_paste"] = paste.url("%s", paste_slug)
        self.content["paste_slug"] = paste_slug

        if self.paste:
            self.get_200()
        else:
            self.get_404()

    def get_200 (self):
        if self.paste.language:
            self.paste.code_colored = self.prepare_code (self.paste.code, self.paste.language)
        self.paste.characters = len(self.paste.code)
        self.paste.lines = self.paste.code.count("\n") + 1
        self.paste.snippet = paste.model.Pasty.make_snippet(self.paste.code, settings.PASTE_SNIPPET_MAX_LENGTH)
        self.paste.put()

        self.write_out("page/pasties/update/200.html")

    def get_404 (self):
        self.write_out("page/pasties/update/404.html")

    def get_paste (self, pasty_slug):
        qry_pastes = paste.model.Pasty.all()
        qry_pastes.filter("slug =", pasty_slug)
        return qry_pastes.get()

    def prepare_code(self, code, language):
        result = ""

        if language != "":
            if "lexer" in smoid.languages.languages[language]:
                lexer_name = smoid.languages.languages[language]["lexer"]
                lexer = pygments.lexers.get_lexer_by_name(lexer_name)
                formatter = paste.syhili.HtmlFormatter(linenos=True, cssclass="code")
                if lexer and formatter:
                    result = pygments.highlight(code, lexer, formatter)

        if result == "":
            result = cgi.escape(code)

        return result

