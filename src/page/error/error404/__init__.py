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
import app.web


class Error404 (app.web.RequestHandler):

    def get (self):
        self.set_module(__name__ + "__init__")
        self.content["http_query"] = self.request.path
        if self.request.query != "":
            self.content["http_query"] = self.content["http_query"] + self.request.query
        self.content["http_query"] = self.content["http_query"]
        self.content["u_paste"] = app.url("")
        self.content["u_pastes"] = app.url("pastes/")

        self.error(404)
        self.use_template("./page.html")
        self.write_out()
