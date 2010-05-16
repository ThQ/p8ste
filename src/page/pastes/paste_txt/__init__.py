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


import cgi

import app.model
import app.web


class PasteTxt (app.web.RequestHandler):

    def get (self, pasty_slug):
        self.set_module(__name__ + ".__init__")
        pasties = app.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)

        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200 (self):
        self.content["content"] = self.pasty.get_raw_code()
        self.set_header("Content-Type", "text/plain")
        self.write_out("./200.tpl")

    def get_404 (self):
        self.write_out("page/txt.tpl")
        self.error(404)
