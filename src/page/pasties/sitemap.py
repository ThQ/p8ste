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
import paste
import paste.model
import paste.web

class Sitemap(paste.web.RequestHandler):
    def __init__(self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.sitemap")

    def get(self):
        self.set_header("Content-Type", "text/xml")

        qry = paste.model.Pasty.all()
        qry.order("-edited_at")
        dbpastes = qry.fetch(100, 0)
        pastes = []

        for dbpaste in dbpastes:
            p = {}
            p["u"] = paste.url("%s", dbpaste.slug)
            p["edited_at"] = dbpaste.edited_at.strftime("%Y-%m-%d")
            p["freq"] = "daily"
            p["priority"] = "0.5"
            pastes.append(p)

        self.content["pastes"] = pastes
        self.use_template("page/pasties/sitemap/200.xml")
        self.write_out()

