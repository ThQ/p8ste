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


import datetime
import cgi

import paste.model
import paste.web


class PastyAtom(paste.web.RequestHandler):
    """
    Displays an atom feed representing the current paste.
    """

    def get(self, pasty_slug):
        self.set_module("page.pasties.pasty_txt.py")
        pasties = paste.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)

        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200(self):
        self.content["paste_title"] = self.pasty.get_title()
        self.content["paste_code"] = self.pasty.get_code()

        self.content["u_paste"] = paste.url("%s", self.pasty.slug)
        self.content["u_paste_self"] = paste.url("%s.atom", self.pasty.slug)
        self.content["paste_username"] = self.pasty.posted_by_user_name
        self.content["paste_posted_at"] = self.pasty.posted_at.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.set_header("Content-Type", "application/atom+xml")
        self.write_out("page/pasties/pasty_atom/200.html")

    def get_404(self):
        self.content["paste_slug"] = self.pasty_slug
        self.content["date"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        self.set_header("Content-Type", "application/atom+xml")
        self.error(404)
        self.write_out("page/pasties/pasty_atom/404.html")
