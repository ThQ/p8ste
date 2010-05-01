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

import app
import app.model
import app.web


class Sitemap (app.web.RequestHandler):

    def __init__ (self):
        app.web.RequestHandler.__init__(self)
        self.set_module(__name__ + "__init__")

    def get (self):
        self.set_header("Content-Type", "text/xml")

        qry = app.model.Pasty.all()
        qry.order("-edited_at")
        dbpastes = qry.fetch(100, 0)
        pastes = []

        for dbpaste in dbpastes:
            p = {}
            p["u"] = app.url("%s", dbpaste.slug)
            p["edited_at"] = dbpaste.edited_at.strftime("%Y-%m-%d")
            p["freq"] = "daily"
            p["priority"] = "0.5"
            pastes.append(p)

        if len(dbpastes) > 0:
            self.content["u_index"] = app.url("pastes/")
            self.content["index_edited_at"] = dbpastes[0].edited_at.strftime("%Y-%m-%d")

        self.content["pastes"] = pastes

        self.write_out("./200.xml")
