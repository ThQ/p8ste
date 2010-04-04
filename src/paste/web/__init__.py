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

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os

import paste

class RequestHandler (webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.module = ""
        self.module_url = ""
        self.content = {}
        self.scripts = []
        self.feeds = []
        self.styles = []

    def add_atom_feed (self, url, title, rel):
        self.add_feed (url, "application/atom+xml", title, rel)

    def add_feed (self, url, type, title, rel):
        feed = {"url":url, "type": type, "title": title, "rel": rel}
        self.feeds.append(feed)

    def set_header(self, name, value):
        if not name in self.response.headers:
            self.response.headers.add_header(name, value)
        else:
            self.response.headers[name] = value

    def set_module(self, name):
        self.module = name.replace(".", "/") + ".py"
        self.module_url = "http://github.com/thomas-quemard/p8ste/blob/master/src/" + self.module
        self.module_history_url = "http://github.com/thomas-quemard/p8ste/commits/master/src/" + self.module

    def use_template(self, name):
        self.template_name = name

    def use_script(self, url):
        self.scripts.append(url)

    def use_style (self, url):
        self.styles.append(url)

    def write_out(self, template_path=""):

        if template_path != "":
            self.use_template(template_path)

        if paste.config["env"] == "debug":
            self.content["debug"] = True
        self.content["header_scripts"] = self.scripts
        self.content["feeds"] = self.feeds
        self.content["styles"] = self.styles
        self.content["module"] = self.module
        self.content["u_home"] = paste.url("")
        self.content["u_pastes"] = paste.url("pastes/")
        self.content["u_module"] = self.module_url
        self.content["u_module_history"] = self.module_history_url
        self.content["u_blank_image"] = paste.url("images/blank.gif")
        user = users.get_current_user()
        if user:
            self.content['user_signed_in'] = True
            self.content['user_email'] = user.email()
            self.content['u_user_logout'] = paste.url("users/signout?url=%s", self.request.url)
        else:
            self.content['user_signed_in'] = False
            self.content['u_user_login'] = paste.url("users/signin?url=%s", self.request.url)

        self.response.out.write(template.render(self.template_name, self.content))


class PasteRequestHandler (RequestHandler):

    def get_paste (self, pasty_slug):
        qry_pastes = paste.model.Pasty.all()
        qry_pastes.filter("slug =", pasty_slug)
        return qry_pastes.get()
