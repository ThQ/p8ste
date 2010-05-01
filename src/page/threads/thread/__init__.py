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

import app
import app.model
import app.web.pastes


class Thread (app.web.pastes.PasteListRequestHandler):
    """
    Show a table of all the pastes in the thread.
    """

    def get (self, paste_slug):
        self.set_module(__name__ + ".__init__")

        self.paste_slug = paste_slug

        self.pastes = self.get_pastes(paste_slug)

        self.content["paste_slug"] = paste_slug


        self.path.add("Pastes", app.url("pastes/"))
        if len(self.pastes) > 0:
            self.get_200()
        else:
            self.get_404()

    def get_200 (self):
        self.path.add(self.paste_slug, app.url("%s", self.paste_slug))
        self.path.add("Thread", app.url("threads/%s", self.paste_slug))
        self.add_atom_feed(app.url("threads/%s.atom", self.paste_slug), "Thread feed", "alternate")

        tpl_pastes = self.templatize_pastes(self.pastes)

        global_size = 0
        global_loc = 0
        for o_paste in self.pastes:
            if o_paste.characters:
                global_size += o_paste.characters
            if o_paste.lines:
                global_loc += o_paste.lines

        self.content["thread_size"] = app.util.make_filesize_readable(global_size)
        self.content["thread_loc"] = global_loc
        self.content["pastes"] = tpl_pastes
        self.content["paste_count"] = len(self.pastes)
        self.write_out("./200.html")

    def get_404 (self):
        self.error(404)
        self.write_out("./404.html")

    def get_pastes (self, paste_slug):
        """
        Fetch all the pastes in the thread.
        """

        qry_pastes = app.model.Pasty.all()
        qry_pastes.filter("thread =", paste_slug)
        qry_pastes.order("-posted_at")

        return qry_pastes.fetch(1000, 0)
