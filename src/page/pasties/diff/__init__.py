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
import difflib

from paste import url
import paste.model
from paste.util import make_filesize_readable
import paste.web
import paste.web.ui
import smoid.languages


class Diff(paste.web.RequestHandler):
    def __init__ (self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.diff.__init__")
        self.use_style(paste.url("style/code.css"))
        self.paste1_slug = ""
        self.paste1 = None
        self.paste2_slug = ""
        self.paste2 = None
        self.pastes = []

    def get (self, paste1_slug, paste2_slug):
        self.paste1_slug = paste1_slug
        self.paste1 = self.get_paste (self.paste1_slug)
        self.paste2_slug = paste2_slug
        self.paste2 = self.get_paste (self.paste2_slug)

        self.pastes = [self.paste1, self.paste2]

        if self.paste1 and self.paste2:
            self.get_200()

    def get_200 (self):
        self.content["u_reverse"] = paste.url(self.paste2_slug + "/diff/" + self.paste1_slug)
        tpl_pastes = [self.get_template_info_for_paste(0), self.get_template_info_for_paste(1)]
        self.content["pastes"] = tpl_pastes
        self.content["diff"] = self.get_diff()
        self.use_template("page/pasties/diff/200.html")
        self.write_out()

    def get_diff (self):
        diff = []
        differ = difflib.Differ()

        lineno1 = 0
        lineno2 = 0
        for line in differ.compare(self.pastes[0].code.splitlines(), self.pastes[1].code.splitlines()):
            if line.startswith("- "):
                lineno1 += 1
                diff.append([lineno1, "", line])
            elif line.startswith("+ "):
                lineno2 += 1
                diff.append(["", lineno2, line])
            else:
                lineno1 += 1
                lineno2 += 1
                diff.append([lineno1, lineno2, line])

        return diff

    def get_paste (self, slug):
        qry_paste = paste.model.Pasty.all()
        qry_paste.filter("slug =", slug)
        return qry_paste.get()

    def get_template_info_for_paste (self, paste_index):
        opaste = self.pastes[paste_index]
        info = {}

        info["slug"] = opaste.slug
        info["posted_at"] = opaste.posted_at.strftime(paste.config["datetime.format"])
        info["u"] = url("%s", opaste.slug)
        info["posted_by"] = opaste.posted_by_user_name

        if opaste.language in smoid.languages.languages:
            info["language"] = smoid.languages.languages[opaste.language]["name"]
            info["u_language_icon"] = smoid.languages.languages[opaste.language]["u_icon"]
        if opaste.characters:
            info["size"] = make_filesize_readable(opaste.characters)
        if opaste.lines:
            info["loc"] = opaste.lines

        return info
