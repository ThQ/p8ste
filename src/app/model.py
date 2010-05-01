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
import random

import app
import smoid.languages


kPASTE_STATUS_PUBLIC = 0
kPASTE_STATUS_PRIVATE = 1
kPASTE_STATUS_MODERATED = 2
kPASTE_STATUS_WAITING_FOR_APPROVAL = 3


class Form (db.Model):
    token           = db.StringProperty()
    created_at      = db.DateTimeProperty()
    created_by_ip   = db.StringProperty()
    expired_at      = db.DateTimeProperty()


class PasteCount (db.Model):
    count = db.IntegerProperty(default=0)
    last_checked = db.DateTimeProperty()
    path = db.StringProperty()


class PasteStats(db.Model):
    paste_count = db.IntegerProperty()
    last_posted_at = db.DateTimeProperty(auto_now=True)
    last_edited_at = db.DateTimeProperty(auto_now=True)


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
    language = db.StringProperty(choices=["html", "java", "perl", "php", "python", "python_console", "ruby", "scala", "sh", "sql", "xml"])
    lines = db.IntegerProperty(default=0)
    posted_at = db.DateTimeProperty()
    posted_by_ip = db.StringProperty(default="")
    posted_by_user_name = db.StringProperty(default="")
    edited_at = db.DateTimeProperty()
    edited_by_ip = db.StringProperty(default="")
    edited_by_user_name = db.StringProperty(default="")
    expired_at = db.DateTimeProperty()
    parent_paste = db.StringProperty(default="")
    secret_key = db.TextProperty(default="")
    slug = db.StringProperty(default="")
    snippet = db.TextProperty(default="")
    tags = db.TextProperty(default="")
    thread = db.StringProperty(default="")
    thread_level = db.IntegerProperty(default=0)
    thread_position = db.IntegerProperty(default=0)
    title = db.TextProperty(default="")
    status = db.IntegerProperty(default=0, choices=[kPASTE_STATUS_PUBLIC, kPASTE_STATUS_PRIVATE, kPASTE_STATUS_MODERATED, kPASTE_STATUS_WAITING_FOR_APPROVAL])
    user = db.ReferenceProperty(User)

    @staticmethod
    def make_secret_key (length = 16):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        char_count = len(chars)
        key = ""
        for i in xrange(0, length):
            pos = random.randint(0, char_count - 1)
            key += chars[pos]
        return key

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

    def get_code (self):
        code = ""
        if self.status == kPASTE_STATUS_PUBLIC:
            code = self.code
        return code

    def get_fork_url (self):
        return app.url("%s/fork", self.slug)

    def get_icon_url (self):
        url = ""

        if self.status == kPASTE_STATUS_PRIVATE:
            url = app.url("images/silk/lock.png")
        elif self.status == kPASTE_STATUS_MODERATED:
            url = app.url("images/silk/flag_red.png")
        elif self.status == kPASTE_STATUS_WAITING_FOR_APPROVAL:
            url = app.url("images/silk/hourglass.png")
        elif self.status == kPASTE_STATUS_PUBLIC:
            if self.language and smoid.languages.languages.has_key(self.language):
                url = app.url("images/languages/" + self.language + ".png")
            else:
                url = app.url("images/silk/page_white_text.png")
        return url

    def get_language_name (self):
        lang = self.language

        if smoid.languages.languages.has_key(lang) and smoid.languages.languages[lang].has_key("name"):
            lang = smoid.languages.languages[lang]["name"]

        return lang

    def get_language_url (self):
        lang = self.language
        url = ""
        if smoid.languages.languages.has_key(lang) and smoid.languages.languages[lang].has_key("home_url"):
            url = smoid.languages.languages[lang]["home_url"]

        return url

    def get_private_url (self):
        return app.url("%s?key=%s", self.slug, self.secret_key)

    def get_title (self):
        """
        Gets the title if there is one and the status allows it.
        """

        title = self.slug
        if self.status == kPASTE_STATUS_PUBLIC and self.title:
            title = self.title
        return title

    def get_snippet (self):
        """
        Gets the snippet if there is one and the status allows it.
        """
        snippet = ""
        if self.snippet:
            if self.status == kPASTE_STATUS_PUBLIC:
                snippet = self.snippet
            elif self.status == kPASTE_STATUS_PRIVATE:
                snippet = "[[ PRIVATE ]]"
        return snippet

    def get_url (self):
        return app.url("%s", self.slug)

    def is_code_viewable (self):
        return self.status == kPASTE_STATUS_PUBLIC

    def is_diffable (self):
        return self.status == kPASTE_STATUS_PUBLIC

    def is_forkable (self):
        return self.status == kPASTE_STATUS_PUBLIC

    def is_private (self):
        return self.status == kPASTE_STATUS_PRIVATE

    def is_public (self):
        return self.status == kPASTE_STATUS_PUBLIC

    def is_moderated (self):
        return self.status == kPASTE_STATUS_MODERATED

    def is_waiting_for_approval (self):
        return self.status == kPASTE_STATUS_WAITING_FOR_APPROVAL

class Log (db.Model):
   type = db.StringProperty(choices=["paste_add", "paste_fork", "user_register"])
   user = db.ReferenceProperty(User)
   item1_slug = db.StringProperty()
   item1_name = db.StringProperty()
   item2_slug = db.StringProperty()
   item2_name = db.StringProperty()
