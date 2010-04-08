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


class IndexAtom(paste.web.RequestHandler):
    """
    A listing of the pastes as an atom feed.
    """

    def __init__(self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.index_atom.__init__")
        self.paste_count = 0

    def get(self):
        self.paste_count = self.get_paste_count()

        self.content["u_pastes"] = paste.url("pastes/")
        self.content["u_self"] = paste.url("pastes.atom")
        self.content["paste_count"] = self.paste_count
        self.content["pastes"] = self.get_pastes()

        self.set_header("Content-Type", "application/atom+xml")
        self.write_out("page/pasties/index_atom/200.html")

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
        dbpastes = db.fetch(10, 0)

        if dbpastes != None:
            for opaste in dbpastes:
                dpaste = {}
                if opaste.title != None or opaste.is_moderated:
                    dpaste["title"] = opaste.title
                else:
                    dpaste["title"] = opaste.slug
                dpaste["u"] = paste.url("%s", opaste.slug)
                dpaste["snippet"] = opaste.snippet
                dpaste["is_moderated"] = opaste.is_moderated

                if opaste.user:
                    dpaste["user_name"] = opaste.user.id
                else:
                    dpaste["user_name"] = opaste.posted_by_user_name

                if opaste.user:
                    dpaste["u_gravatar"] = opaste.user.get_gravatar(16)

                if opaste.language and opaste.language in smoid.languages.languages:
                    dpaste["u_language_icon"] = smoid.languages.languages[opaste.language]['u_icon']

                if opaste.forks > 0:
                    dpaste["forks"] = opaste.forks

                if opaste.posted_at != None:
                    dpaste["posted_at"] = opaste.posted_at.strftime(paste.config["datetime.atom"])
                else:
                    dpaste["posted_at"] = ""

                if opaste.characters:
                    dpaste["size"] = paste.util.make_filesize_readable(opaste.characters)
                dpaste["lines"] = opaste.lines
                if opaste.language:
                    dpaste["language"] = opaste.language
                else:
                    dpaste["language"] = ""

                pastes.append(dpaste)
        return pastes
