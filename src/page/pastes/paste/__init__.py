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

    def update_highlights (self, hl_string):
        line_max = self.line_count + 1
        if hl_string != "":
            hl_items = hl_string.split(",")
            for item in hl_items:
                if item.isdigit():
                    self.highlights.add(int(item))

                # Line range
                elif ":" in item != -1:
                    part = item.partition(":")
                    if part[0].isdigit() and part[2].isdigit():
                        r_start = int(part[0])
                        r_end = int(part[2]) + 1
                        if r_start > r_end :
                            t_end = r_end
                            r_end = t_end
                            r_start = t_end
                        if r_start > line_max : r_start = line_max
                        if r_end > line_max : r_end = line_max

                        if r_start != r_end and not (r_start == 1 and r_end == line_max):
                            for i in range(r_start, r_end):
                                if not i in self.highlights:
                                    self.highlights.add(i)

                # Reset
                elif item == "-":
                    self.highlights = []

                # Reverse
                elif item == "!":
                    rhl = [hl_string]
                    for i in range(1, line_max):
                        if not i in hl:
                            rhl.add(i)
                    self.highlights = rhl
        return self.highlights

    def format_code(self):
        r_code = ""
        r_lines = ""
        i = 1
        for line in self.lines:
            #r_lines += "<tr><td class=\"line\">"
            r_lines += "<a href=\"#l" + str(i) + "\" name=\"l" + str(i) + "\">" + str(i) + "</a>\n"
            #r_lines += "</td></tr>\n"

            #r_code += "<tr>"
            #if i in self.highlights: r_code += "<td class=\"hl\">"
            #else: r_code += "<td>"

            if self.has_edited_lines and self.edited_lines.has_key(str(i)):
                r_code += self.format_line_start(cgi.escape(self.request.get("e" + str(i))))
            else:
                if line == "": r_code += "\n"
                else: r_code += self.format_line_start(line)

            #r_code += "</td></tr>\n"
            i += 1

        return (r_lines, r_code)

    def format_simple_code(self):
        r_lines = ""
        r_code = ""
        i = 1
        for line in self.lines:
            #r_lines += "<tr><td class=\"line\"><a href=\"#l" + str(i) + "\" name=\"l" + str(i) + "\">" + str(i) + "</a></td></tr>"
            r_lines += "<a href=\"#l" + str(i) + "\" name=\"l" + str(i) + "\">" + str(i) + "</a>\n"
            #r_code += "<tr><td>"
            if line == "": r_code += "\n"
            else: r_code += self.format_line_start(line) + "\n"
            #r_code += "</td></tr>\n"
            i += 1
        return (r_lines, r_code)

    def format_line_start(self, line):
        result = ""
        i = 0
        for c in line:
            if c == " ":
                result += "&nbsp;"
            elif c == "\t":
                result += "&nbsp;&nbsp;&nbsp;"
            else:
                result += line[i:]
                break;
            i += 1
        return result

    def get(self, pasty_slug):
        pasties = app.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)
        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug
        self.get_parent_paste()

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200(self):
        self.secret_key = self.request.get("key")
        user_is_poster = (self.pasty.user and self.user.db_user and self.pasty.user.id == self.user.db_user.id)

        if self.pasty.is_private() and (self.secret_key == self.pasty.secret_key or user_is_poster):
            self.paste_title = self.pasty.title
            self.code_is_viewable = True
        else:
            self.paste_title = self.pasty.get_title()
            self.code_is_viewable = self.pasty.is_code_viewable()

        self.path.add(self.paste_title, self.pasty.get_url())

        self.lines = self.pasty.code_colored.splitlines()
        self.line_count = len(self.lines)
        lines = ""
        code = ""

        complex_formating = self.request.get("h") != ""

        if self.request.get("h"):
            self.update_highlights(self.request.get("h"))

        for arg in self.request.arguments():
            if arg[0:1] == "e" and arg[1:].isdigit():
                self.edited_lines[arg[1:]] = True
                self.has_edited_lines = True
                complex_formating = True

        if complex_formating:
            (lines, code) = self.format_code()
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
        tpl_paste["loc"] = self.pasty.lines
        tpl_paste["lines"] = lines
        tpl_paste["code"] = code
        tpl_paste["size"] = app.util.make_filesize_readable(self.pasty.characters)
        tpl_paste["pasted_at"] = self.pasty.posted_at.strftime(settings.DATETIME_FORMAT)
        tpl_paste["is_moderated"] = self.pasty.is_moderated()
        tpl_paste["is_private"] = self.pasty.is_private()
        tpl_paste["is_waiting_for_approval"] = self.pasty.is_waiting_for_approval()
        tpl_paste["is_code_viewable"] = self.code_is_viewable

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
        self.content["page-title"] =  self.paste_title
        self.content["pasty_title"] =  self.paste_title
        self.content["pasty_slug"] = self.pasty.slug
        self.content["pasty_is_moderated"] = self.pasty.is_moderated
        self.content["is_code_viewable"] = self.code_is_viewable
        self.content["is_private"] = self.pasty.is_private()
        self.content["is_public"] = self.pasty.is_public()
        self.content["is_diffable"] = self.pasty.is_diffable()
        self.content["user_name"] = self.pasty.posted_by_user_name
        if self.pasty.user:
            self.content["u_user"] = app.url("users/%s", self.pasty.user.id)
            self.content["u_gravatar"] = self.pasty.user.get_gravatar(48)

        self.content["posted_at"] = self.pasty.posted_at.strftime("%b, %d %Y at %H:%M")
        if self.pasty.language:
            lang = smoid.languages.languages[self.pasty.language]
            self.content["pasty_language_url"] = lang["home_url"]

        self.add_atom_feed(app.url("%s.atom", self.pasty_slug), self.pasty_slug + " (Atom feed)", "alternate")
        self.write_out("./200.html")

        #self.update_expiration_time()

    def get_404(self):
        self.path.add("Paste not found")
        self.error(404)
        self.content["pasty_slug"] = cgi.escape(self.pasty_slug)
        self.content["u_paste"] = app.url("")
        self.content["u_pastes"] = app.url("pastes/")
        self.write_out("./404.html")

    def get_parent_paste(self):
        if self.pasty != None and self.pasty.parent_paste != "":
            qparent = app.model.Pasty.all()
            qparent.filter("slug =", self.pasty.parent_paste)
            self.parent = qparent.get()
            if self.parent != None:
                self.content["u_parent"] = app.url("%s", self.parent.slug)
                self.content["parent_title"] = cgi.escape(self.parent.title)

            # Datastore is not up to date, removing <parent_paste> slug
            # because the parent has been deleted
            else:
                self.pasty.parent_paste = ""
                self.pasty.put()

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
                list_opened -= 1
            pastes.append(lpaste)

        self.content["lists_unclosed"] = xrange(0, lists_opened)

        return pastes
