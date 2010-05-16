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
import logging

import app
import app.lang
import app.model
import app.util
import app.web
import settings
import smoid.languages


class Paste (app.web.RequestHandler):

    def __init__ (self):
        app.web.RequestHandler.__init__(self)
        self.set_module(__name__ + ".__init__")
        self.use_style(app.url("style/code.css"))
        self.highlights = set([])
        self.has_edited_lines = False
        self.has_highlights = False
        self.edited_lines = {}
        self.lines = []
        self.line_count = 0
        self.parent = None
        self.path.add("Pastes", app.url("pastes/"))

    def format_complex_code (self, highlights):
        r_code = ""
        r_lines = ""

        for i, line in enumerate(self.lines):
            r_lines += "<a href=\"#l" + str(i) + "\" name=\"l" + str(i) + "\">" + str(i) + "</a>\n"

            if str(i) in highlights:
                r_code += """<span class="hl">""" + line + "</span>\n"
            else:
                r_code += self.format_line_start(line) + "\n"

        return (r_lines, r_code)

    def format_line_start (self, line):
        """
        Make whitespaces print right in HTML:
        * Replace spaces with <&nbsp;>
        * Replace tabs with three <&nbsp;>
        """
        result = ""

        for i, char in enumerate(line):
            if char == " ":
                result += "&nbsp;"
            elif char == "\t":
                result += "&nbsp;&nbsp;&nbsp;"
            else:
                result += line[i:]
                break

        return result

    def format_simple_code(self):
        """
        Make whitespaces at line starts print right in HTML.
        """

        r_lines = ""
        r_code = ""

        for i, line in enumerate(self.lines):
            r_lines += "<a href=\"#l" + str(i) + "\" name=\"l" + str(i) + "\">"
            r_lines += str(i)
            r_lines += "</a>\n"

            if line == "":
                r_code += "\n"
            else:
                r_code += self.format_line_start(line) + "\n"

        return (r_lines, r_code)

    def get (self, pasty_slug):
        pasties = app.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)
        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug
        self.get_parent_paste()

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200 (self):
        self.secret_key = self.request.get("key")
        user_is_poster = (self.pasty.user and self.user.db_user and self.pasty.user.id == self.user.db_user.id)

        self.lines = self.pasty.code_colored.splitlines()
        lines = ""
        code = ""

        complex_formating = self.pasty.highlights != ""

        if complex_formating:
            (lines, code) = self.format_complex_code(self.pasty.highlights)
        else:
            (lines, code) = self.format_simple_code()

        if self.pasty.parent_paste or self.pasty.forks > 0:
            thread_pastes = self.get_thread_pastes()
        else:
            thread_pastes = []

        tpl_paste = {}
        tpl_paste["u"] = self.pasty.get_url()
        tpl_paste["u_fork"] = self.pasty.get_fork_url()
        tpl_paste["u_raw_text"] = app.url("%s.txt", self.pasty_slug)
        tpl_paste["u_atom"] = app.url("%s.atom", self.pasty_slug)
        tpl_paste["slug"] = self.pasty.slug
        tpl_paste["title"] = self.pasty.get_title()
        tpl_paste["loc"] = self.pasty.lines
        tpl_paste["lines"] = lines
        tpl_paste["code"] = code
        tpl_paste["size"] = app.util.make_filesize_readable(self.pasty.characters)
        tpl_paste["pasted_at"] = self.pasty.posted_at.strftime(settings.DATETIME_FORMAT)
        tpl_paste["is_moderated"] = self.pasty.is_moderated()
        tpl_paste["is_private"] = self.pasty.is_private()
        tpl_paste["is_public"] = self.pasty.is_public()
        tpl_paste["is_waiting_for_approval"] = self.pasty.is_waiting_for_approval()
        tpl_paste["is_code_viewable"] = self.pasty.is_code_viewable()

        tpl_paste["language"] = {}
        tpl_paste["language"]["u"] = self.pasty.get_language_url()
        tpl_paste["language"]["u_icon"] = self.pasty.get_icon_url()
        tpl_paste["language"]["name"] = self.pasty.get_language_name()

        tpl_paste["thread"] = {}
        tpl_paste["thread"]["length"] = len(thread_pastes)

        self.content["paste"] = tpl_paste
        self.content["is_thread"] = len(thread_pastes) > 1
        self.content["thread_paste_count"] = len(thread_pastes)
        self.content["u_thread_atom"] = app.url("threads/%s.atom", self.pasty.thread)
        self.content["u_thread"] = app.url("threads/%s", self.pasty.thread)
        self.content["u_remote_diff"] = app.url("%s/diff", self.pasty.slug)
        if self.content["is_thread"] == True:
            self.content["thread_pastes"] = thread_pastes
        self.content["h1"] = "p" + self.pasty_slug
        self.content["user_name"] = self.pasty.posted_by_user_name
        if self.pasty.user:
            self.content["u_user"] = app.url("users/%s", self.pasty.user.id)
            self.content["u_gravatar"] = self.pasty.user.get_gravatar(48)

        self.content["posted_at"] = self.pasty.posted_at.strftime("%b, %d %Y at %H:%M")
        if self.pasty.language:
            lang = smoid.languages.languages[self.pasty.language]
            self.content["pasty_language_url"] = lang["home_url"]

        self.add_atom_feed(app.url("%s.atom", self.pasty_slug), self.pasty_slug + " (Atom feed)", "alternate")
        self.path.add(self.pasty.get_title(), self.pasty.get_url())
        self.write_out("./200.html")

    def get_404 (self):
        self.path.add("Paste not found")
        self.error(404)
        self.content["pasty_slug"] = cgi.escape(self.pasty_slug)
        self.content["u_paste"] = app.url("")
        self.content["u_pastes"] = app.url("pastes/")
        self.write_out("./404.html")

    def get_parent_paste (self):
        if self.pasty != None and self.pasty.parent_paste != "":
            qparent = app.model.Pasty.all()
            qparent.filter("slug =", self.pasty.parent_paste)
            self.parent = qparent.get()

    def get_thread_pastes (self):
        default_chars = self.pasty.characters
        default_loc = self.pasty.lines

        pastes = []
        dbqry = app.model.Pasty.all()
        dbqry.filter("thread =", self.pasty.thread)
        dbqry.order("thread_position")
        dbpastes = dbqry.fetch(1000)

        cur_level = 0
        paste_count = len(dbpastes)
        i = 1
        lists_opened = 0
        for dbpaste in dbpastes:
            lpaste = {}
            lpaste["title"] = dbpaste.title
            lpaste["slug"] = dbpaste.slug
            lpaste["user_name"] = dbpaste.posted_by_user_name
            lpaste["is_moderated"] = dbpaste.is_moderated
            lpaste["u"] = dbpaste.get_url()
            lpaste["u_diff"] = app.url("%s/diff/%s", self.pasty.slug, dbpaste.slug)
            lpaste["ident"] = ("&nbsp;&nbsp;&nbsp;&nbsp;" * dbpaste.thread_level)

            lpaste["language_name"] = dbpaste.get_language_name()
            lpaste["u_language_image"] = dbpaste.get_icon_url()

            if dbpaste.characters > default_chars:
                lpaste["diff_size"] = app.util.make_filesize_readable(dbpaste.characters - default_chars)
                lpaste["diff_size"].append("+")
            else:
                lpaste["diff_size"] = app.util.make_filesize_readable(default_chars - dbpaste.characters)
                lpaste["diff_size"].append("-")

            if dbpaste.lines > default_loc:
                lpaste["diff_loc"] = "+"
            else:
                lpaste["diff_loc"] = ""
            lpaste["diff_loc"] += str(dbpaste.lines - default_loc)

            if dbpaste.thread_level > cur_level:
                cur_level = dbpaste.thread_level
                lpaste["open_list"] = 1
                lists_opened += 1
            elif dbpaste.thread_level < cur_level:
                cur_level = dbpaste.thread_level
                lpaste["close_list"] = 1
                lists_opened -= 1
            pastes.append(lpaste)

        self.content["lists_unclosed"] = xrange(0, lists_opened)

        return pastes
