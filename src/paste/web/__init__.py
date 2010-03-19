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
import paste.log

class RequestHandler (webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.module = ""
        self.module_url = ""
        self.content = {}
        self.scripts = []

    def set_header(self, name, value):
        if not name in self.response.headers:
            self.response.headers.add_header(name, value)
        else:
            self.response.headers[name] = value

    def set_module(self, name):
        self.module = name.replace(".", "/") + ".py"
        self.module_url = "http://code.google.com/p/paste-it/source/browse/trunk/src/" + self.module

    def use_template(self, name):
        self.template_name = name

    def use_script(self, url):
        self.scripts.append(url)

    def write_out(self, template_path=""):

        if template_path != "":
            self.use_template(template_path)

        if paste.config["env"] == "debug":
            self.content["debug"] = True
        self.content["header_scripts"] = self.scripts
        self.content["module"] = self.module
        self.content["u_module"] = self.module_url
        self.content["u_blank_image"] = paste.url("images/blank.gif")
        user = users.get_current_user()
        if user:
            self.content['user_signed_in'] = True
            self.content['user_email'] = user.email()
            self.content['u_user_logout'] = users.create_logout_url(paste.url("a"))
        else:
            self.content['user_signed_in'] = False
            self.content['u_user_login'] = users.create_login_url(paste.url("a"))

        logs = []
        for logrec in paste.log.DebugHandler.logs:
            log = {}
            log["message"] = logrec.getMessage()
            log["path"] = logrec.pathname
            log["path_with_line"] = logrec.pathname + ":" + str(logrec.lineno)
            logs.append(log)
        self.content["logs"] = logs

        self.response.out.write(template.render(self.template_name, self.content))

        paste.log.DebugHandler.logs = []
