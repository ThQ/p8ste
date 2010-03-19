#!/usr/bin/env python
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
import os
import paste
import paste.web

class Error404(paste.web.RequestHandler):
    def get(self):
        self.content["http_query"] = self.request.path
        if self.request.query != "":
            self.content["http_query"] = self.content["http_query"] + self.request.query
        self.content["http_query"] = cgi.escape(self.content["http_query"])
        self.content["u_paste"] = paste.url("")
        self.content["u_pastes"] = paste.url("pastes/")

        self.error(404)
        self.use_template("page/error/error404/page.html")
        self.write_out()
