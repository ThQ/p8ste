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


class Pasty (db.Model):
    characters = db.IntegerProperty()
    code = db.TextProperty()
    code_colored = db.TextProperty()
    forks = db.IntegerProperty()
    indirect_forks = db.IntegerProperty()
    language = db.StringProperty(choices=["php", "python"])
    lines = db.IntegerProperty()
    posted_at = db.DateTimeProperty(auto_now=True)
    posted_by_ip = db.StringProperty()
    posted_by_user_name = db.StringProperty()
    edited_at = db.DateTimeProperty(auto_now=True)
    edited_by_ip = db.StringProperty()
    edited_by_user_name = db.StringProperty()
    expired_at = db.DateTimeProperty()
    parent_paste = db.StringProperty()
    slug = db.StringProperty()
    snippet = db.TextProperty()
    tags = db.TextProperty()
    thread = db.StringProperty()
    thread_level = db.IntegerProperty()
    thread_position = db.IntegerProperty()
    title = db.TextProperty()

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
