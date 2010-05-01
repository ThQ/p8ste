#_slug Copyright 2008 Thomas Quemard
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
import datetime
import logging

import smoid.languages
import app
import app.lang
import app.model
import app.util
import app.web
import app.web.pastes
import app.web.ui

class List (app.web.pastes.PasteListRequestHandler):

    def __init__ (self):
        app.web.RequestHandler.__init__(self)
        self.set_module(__name__ + ".__init__")
        self.use_style(app.url("style/code.css"))
        self.parent = None
        self.pastes = []
        self.paste_count = 0
        self.paste_sep = "%2B"

    def get (self, slugs):
        self.paste_slugs = set(slugs.split(self.paste_sep))

        # Retrieve the pastes from the datastore
        for slug in self.paste_slugs:
            slug = slug.strip()
            if slug != "":
                p = self.get_paste(slug)
                if p != None:
                    self.pastes.append(p)

        self.paste_count = len(self.pastes)
        if self.paste_count == 1:
            self.redirect(app.url("%s", self.pastes[0].slug))
        elif self.paste_count > 0:
            self.get_200()
        else:
            self.get_404()

    def get_200 (self):
        """
        At least two pastes have been found in the list.
        """

        self.tpl_pastes = self.templatize_pastes (self.pastes)

        global_size = 0
        global_line_count = 0
        ui_code = app.web.ui.Code()
        i = 0
        for p in self.pastes:
            line_nos, code_lines = ui_code.format_code(p.code_colored)
            self.tpl_pastes[i]["lines"] = line_nos
            self.tpl_pastes[i]["code"] = code_lines
            global_size += p.characters
            global_line_count += p.lines
            i += 1

        self.content["pastes"] = self.tpl_pastes
        self.content["global_size"] = app.util.make_filesize_readable(global_size)
        self.content["global_line_count"] = global_line_count

        self.write_out("./200.html")

    def get_404 (self):
        """
        No paste (none) has been found.
        """

        self.error(404)
        self.write_out("./404.html")
