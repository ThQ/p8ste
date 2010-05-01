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

import app.model
import app.web


class ThreadAtom (app.web.RequestHandler):

    def get (self, pasty_slug):
        self.set_module(__name__ + ".__init__")
        pasties = app.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)

        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug
        self.forks = []

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200 (self):
        self.get_forks()

        self.content["paste_title"] = self.pasty.get_title()
        self.content["paste_code"] = self.pasty.get_code()

        self.content["u_thread"] = app.url("threads/%s", self.pasty.slug)
        self.content["u_thread_self"] = app.url("threads/%s.atom", self.pasty.slug)
        self.content["paste_username"] = self.pasty.posted_by_user_name
        self.content["paste_posted_at"] = self.pasty.posted_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.content["forks"] = self.forks

        self.set_header("Content-Type", "application/atom+xml")
        self.write_out("page/threads/thread_atom/200.html")

    def get_404 (self):
        self.content["paste_slug"] = self.pasty_slug
        self.content["u_thread"] = app.url("threads/%s", self.pasty_slug)
        self.content["u_thread_self"] = app.url("threads/%s.atom", self.pasty_slug)
        self.content["date"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        self.set_header("Content-Type", "application/atom+xml")
        self.error(404)
        self.write_out("page/threads/thread_atom/404.html")

    def get_forks (self):
        qry_forks = app.model.Pasty.all()
        qry_forks.filter("thread =", self.pasty.slug)
        qry_forks.order("-posted_at")
        db_forks = qry_forks.fetch (10)

        if db_forks:
            for db_fork in db_forks:
                tpl_fork = {}
                tpl_fork["u"] = db_fork.get_url()
                tpl_fork["slug"] = db_fork.slug
                tpl_fork["title"] = db_fork.get_title()
                tpl_fork["published_at"] = db_fork.posted_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                tpl_fork["updated_at"] = db_fork.edited_at.strftime("%Y-%m-%dT%H:%M:%SZ")
                tpl_fork["author_name"] = db_fork.posted_by_user_name
                tpl_fork["summary"] = db_fork.get_snippet()
                self.forks.append(tpl_fork)
