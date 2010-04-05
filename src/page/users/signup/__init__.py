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
from google.appengine.api import users

import paste.model
import paste.web


class SignUp (paste.web.RequestHandler):

    def get (self):
        self.set_module("page.users.signup.__init__")

        self.content["u_signup"] = paste.url("sign-up")

        if self.user.is_logged_in:
            self.write_out("page/users/signup/already_logged_in.html")
        else:
            if not self.user.is_logged_in_google or self.request.get("user_id") == "":
                self.content["google_email"] = self.user.google_email
                self.content["u_google_login"] = users.create_login_url(paste.url("sign-up"))
                self.get_form()
            else:
                self.get_form_sent()

    def get_form (self):
        self.write_out("page/users/signup/form.html")

    def get_form_sent (self):
        self.put_user()
        self.write_out("page/users/signup/done.html")

    def post (self):
        self.get()

    def put_user (self):
        db_user = paste.model.User()
        db_user.id = self.request.get("user_id")
        db_user.google_id = self.user.google_id
        db_user.email = self.user.google_email
        db_user.gravatar_id = self.user.gravatar_id
        db_user.paste_count = 0
        db_user.registered_at = datetime.datetime.now()

        return db_user.put()

    def validate_user_id (self, id):
        result = True
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        for c in id:
            if not c in valid_chars:
                result = False
                break
        return result
