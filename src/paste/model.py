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

from google.appengine.ext import db

class Form (db.Model):
    token = db.StringProperty()
    created_at = db.DateTimeProperty()
    created_by_ip = db.StringProperty()
    expired_at = db.DateTimeProperty()


class PasteReply (db.Model):
    parent_paste = db.StringProperty()
    reply = db.StringProperty()
    title = db.TextProperty()

class PasteTag (db.Model):
    pasty_slug = db.StringProperty()
    tag_slug = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now=True)
    created_by_ip = db.StringProperty()
    edited_at = db.DateTimeProperty(auto_now=True)
    edited_by_ip = db.StringProperty()


class PasteCount (db.Model):
    count = db.IntegerProperty(default=0)
    last_checked = db.DateTimeProperty()
    path = db.StringProperty()

class PasteStats(db.Model):
    paste_count = db.IntegerProperty()
    last_posted_at = db.DateTimeProperty(auto_now=True)
    last_edited_at = db.DateTimeProperty(auto_now=True)

class Tag(db.Model):
    slug = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now=True)
    created_by_ip = db.StringProperty()
    edited_at = db.DateTimeProperty(auto_now=True)
    edited_by_ip = db.StringProperty()
    pastes = db.IntegerProperty()

class User (db.Model):
    id = db.StringProperty()
    google_id = db.StringProperty()
    email = db.StringProperty()
    gravatar_id = db.TextProperty()
    paste_count = db.IntegerProperty()
    registered_at = db.DateTimeProperty()

    def get_gravatar (self, size):
        return "http://www.gravatar.com/avatar/" + self.gravatar_id + ".jpg?s=" + str(size)

class Pasty (db.Model):
    characters = db.IntegerProperty(default=0)
    code = db.TextProperty(default="")
    code_colored = db.TextProperty(default="")
    forks = db.IntegerProperty(default=0)
    indirect_forks = db.IntegerProperty(default=0)
    is_moderated = db.BooleanProperty(default=False)
    language = db.StringProperty(choices=["java", "perl", "php", "python", "python_console", "ruby", "scala", "sh", "xml"])
    lines = db.IntegerProperty(default=0)
    posted_at = db.DateTimeProperty()
    posted_by_ip = db.StringProperty(default="")
    posted_by_user_name = db.StringProperty(default="")
    edited_at = db.DateTimeProperty()
    edited_by_ip = db.StringProperty(default="")
    edited_by_user_name = db.StringProperty(default="")
    expired_at = db.DateTimeProperty()
    parent_paste = db.StringProperty(default="")
    slug = db.StringProperty(default="")
    snippet = db.TextProperty(default="")
    tags = db.TextProperty(default="")
    thread = db.StringProperty(default="")
    thread_level = db.IntegerProperty(default=0)
    thread_position = db.IntegerProperty(default=0)
    title = db.TextProperty(default="")
    user = db.ReferenceProperty(User)

    @staticmethod
    def make_snippet (code, snippet_len):
        snippet = ""
        newline_block = False
        char_count = 0
        last_char = ""
        whitespaces = ["\n", "\r", "\t", " "]

        for c in code:
            if c in whitespaces:
                if last_char != " ":
                    snippet += " "
                    last_char = " "
                    char_count += 1
            else:
                snippet += c
                last_char = c
                char_count += 1

            if char_count > snippet_len:
                snippet = snippet[0: char_count - 3] + "..."
                break

        return snippet
