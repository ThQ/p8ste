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


import cgi
from google.appengine.api import users

import app.model
import app.web


class User (app.web.UserRequestHandler):

    def get (self, user_id):
        self.set_module(__name__ + ".__init__")
        self.db_user = self.get_user(user_id)
        self.content["user_name"] = user_id

        if self.db_user:
            self.get_200()
        else:
            self.get_404()

    def get_200 (self):
        self.write_out("./200.html")

    def get_404 (self):
        self.error(404)
        self.write_out("./404.html")
