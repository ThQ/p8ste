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
import datetime
import difflib
import google.appengine.api.urlfetch
import logging

import smoid.languages
import app
import app.model
import app.util
import app.web
import app.web.pastes
import app.web.ui


class RemoteDiff (app.web.pastes.PasteRequestHandler):
    """
    Displays a diff between a local paste and a remote file.
    """

    def __init__ (self):
        app.web.RequestHandler.__init__(self)
        self.set_module(__name__ + ".__init__")
        self.use_style(app.url("style/code.css"))
        self.paste = None


    def fetch_url (self):
        content = None
        try:
            resp = google.appengine.api.urlfetch.fetch(self.remote_url, allow_truncated=True, deadline=10)
            if resp != None:
               content = resp.content
        except google.appengine.api.urlfetch.Error:
            pass
        return content

    def get (self, slug):
        self.paste = self.get_paste(slug)
        self.paste_slug = slug
        self.content["paste_slug"] = self.paste_slug
        self.content["u_paste"] = app.url("%s", slug)

        if self.paste:

            self.path.add("Pastes", app.url("pastes/"))
            self.path.add(self.paste.get_title(), self.paste.get_url())

            if self.paste.is_public():
                self.remote_url = self.request.get("url")
                if self.remote_url[0:7] != "http://":
                    self.remote_url = "http://" + self.remote_url

                self.remote_content = self.fetch_url()
                self.content["remote_url"] = self.remote_url

                if self.remote_content:
                    self.get_200()
                else:
                    self.get_404_remote()
            else:
                self.content["paste_is_private"] = self.paste.is_private()
                self.content["paste_is_moderated"] = self.paste.is_moderated()
                self.content["paste_is_awaiting_approval"] = self.paste.is_waiting_for_approval()
                self.error(401)
                self.write_out("template/paste/not_public.html")
        else:
            self.get_404_paste()

    def get_200 (self):
        self.content["diff"] = self.get_diff()
        self.content["paste_title"] = self.paste.title
        self.content["paste_size"] = app.util.make_filesize_readable(self.paste.characters)
        self.content["paste_loc"] = self.paste.lines
        self.write_out("./200.html")

    def get_404_paste (self):
        self.write_out("./404_paste.html")

    def get_404_remote (self):
        self.write_out("./404_remote.html")

    def get_diff (self):
        """
        Compute a diff and annotate each line with a line number.
        """

        paste_content = self.paste.code
        remote_content = self.remote_content

        diff = []
        differ = difflib.Differ()

        lineno1 = 0
        lineno2 = 0

        for line in differ.compare(paste_content.splitlines(), remote_content.splitlines()):
            line_start = line[0:2]

            if line_start == "- ":
                lineno1 += 1
                diff.append([lineno1, "", '<span class="cmt">-</span> ' + line[2:]])

            elif line_start == "+ ":
                lineno2 += 1
                diff.append(["", lineno2, '<span class="cmt">+</span> ' + cgi.escape(line[2:])])

            else:
                lineno1 += 1
                lineno2 += 1
                diff.append([lineno1, lineno2, line])

        return diff
