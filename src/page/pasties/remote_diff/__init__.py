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
import paste
import paste.lang
import paste.model
import paste.util
import paste.web
import paste.web.pastes
import paste.web.ui

class RemoteDiff (paste.web.pastes.PasteRequestHandler):

    def __init__ (self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.remote_diff.__init__")
        self.use_style(paste.url("style/code.css"))
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
        self.content["u_paste"] = paste.url("%s", slug)
        if self.paste:
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
            self.get_404_paste()

    def get_200 (self):
        self.content["diff"] = self.get_diff()
        self.content["paste_title"] = self.paste.title
        self.content["paste_size"] = paste.util.make_filesize_readable(self.paste.characters)
        self.content["paste_loc"] = self.paste.lines
        self.write_out("page/pasties/remote_diff/200.html")

    def get_404_paste (self):
        self.write_out("page/pasties/remote_diff/404_paste.html")

    def get_404_remote (self):
        self.write_out("page/pasties/remote_diff/404_remote.html")

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
                diff.append([lineno1, "", '<span class="cmt">-</span> ' + line[3:]])

            elif line_start == "+ ":
                lineno2 += 1
                diff.append(["", lineno2, '<span class="cmt">+</span> ' + line[3:]])

            else:
                lineno1 += 1
                lineno2 += 1
                diff.append([lineno1, lineno2, line])

        return diff
