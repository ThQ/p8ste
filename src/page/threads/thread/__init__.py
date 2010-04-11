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

import paste
import paste.model
import paste.web.pastes


class Thread (paste.web.pastes.PasteListRequestHandler):

    def get(self, paste_slug):
        self.set_module("page.threads.thread.__init__")

        self.paste_slug = paste_slug

        self.pastes = self.get_pastes(paste_slug)

        self.content["paste_slug"] = paste_slug

        if len(self.pastes) > 0:
            self.get_200()
        else:
            self.get_404()

    def get_200(self):
        self.add_atom_feed(paste.url("threads/%s.atom", self.paste_slug), "Thread feed", "alternate")

        tpl_pastes = self.templatize_pastes(self.pastes)

        global_size = 0
        global_loc = 0
        for o_paste in self.pastes:
            if o_paste.characters:
                global_size += o_paste.characters
            if o_paste.lines:
                global_loc += o_paste.lines

        self.content["thread_size"] = paste.util.make_filesize_readable(global_size)
        self.content["thread_loc"] = global_loc
        self.content["pastes"] = tpl_pastes
        self.content["paste_count"] = len(self.pastes)
        self.write_out("page/threads/thread/200.html")

    def get_404(self):
        self.error(404)
        self.write_out("page/threads/thread/404.html")

    def get_pastes (self, paste_slug):
        """
        Fetch all the pastes in the thread.
        """

        qry_pastes = paste.model.Pasty.all()
        qry_pastes.filter("thread =", paste_slug)
        qry_pastes.order("-posted_at")

        return qry_pastes.fetch(1000, 0)
