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
import paste
import paste.model
import paste.util
import paste.web
import paste.web.ui
import smoid.languages


class Index(paste.web.RequestHandler):
    """
    A listing of the pastes.
    """

    def __init__(self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.index.__init__")
        self.page = 1
        self.pastes_per_page = 10
        self.paste_count = 0

    def get(self):
        self.path.add("Pastes", paste.url("pastes/"))

        if self.request.get("page").isdigit() and int(self.request.get("page")) > 1:
            self.page = int(self.request.get("page"))

        pastes = self.get_pastes()
        self.paste_count = self.get_paste_count()

        paging = self.make_paging()

        if paging.page_count > 1:
            self.content["pages"] = paging.pages

        self.content["paste_start"] = ((self.page - 1) * self.pastes_per_page) + 1
        self.content["paste_end"] = self.content["paste_start"] - 1 + len(pastes)
        self.content["paste_count"] = self.paste_count
        self.content["pastes"] = pastes

        self.add_atom_feed(paste.url("pastes.atom"), "Last pastes", "alternate")
        self.write_out("page/pasties/index/200.html")

    def get_paste_count (self):
        """
        Retrieve the total paste count from the datastore.
        """

        count = 0
        stats = paste.model.PasteStats.all()
        stats.id = 1
        stat = stats.get()
        if stat != None:
            count = stat.paste_count
        return count

    def get_pastes (self):
        """
        Retrieve the pastes for the current page.
        """

        pastes = []

        db = paste.model.Pasty.all()
        db.order("-posted_at")
        dbpastes = db.fetch(self.pastes_per_page, (self.page - 1) * self.pastes_per_page)

        if dbpastes != None:
            for opaste in dbpastes:
                dpaste = {}
                dpaste["title"] = opaste.get_title()
                dpaste["u"] = opaste.get_url()
                dpaste["snippet"] = opaste.get_snippet()

                if opaste.user:
                    dpaste["u_user"] = paste.url("users/%s", opaste.user.id)
                dpaste["user_name"] = opaste.posted_by_user_name

                if opaste.user:
                    dpaste["u_gravatar"] = opaste.user.get_gravatar(16)

                dpaste["u_language_icon"] = opaste.get_icon_url()

                if opaste.forks > 0:
                    dpaste["forks"] = opaste.forks

                if opaste.posted_at != None:
                    dpaste["posted_at"] = opaste.posted_at.strftime(paste.config["datetime.format"])
                else:
                    dpaste["posted_at"] = ""

                if opaste.characters:
                    dpaste["size"] = paste.util.make_filesize_readable(opaste.characters)
                dpaste["lines"] = opaste.lines
                if opaste.language:
                    dpaste["language"] = opaste.get_language_name()
                else:
                    dpaste["language"] = ""

                pastes.append(dpaste)
        return pastes

    def make_paging (self):
        """
        Makes the paging UI component.
        """

        paging = paste.web.ui.CursorPaging()
        paging.page = self.page
        paging.items = self.paste_count
        paging.page_length = 10
        paging.left_margin = 2
        paging.right_margin = 2
        paging.cursor_margin = 1
        paging.page_url = paste.url("pastes/?page={page}")
        paging.prepare()

        return paging
