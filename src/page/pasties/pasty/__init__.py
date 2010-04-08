#_slug Copyright 2008 Thomas Quemard
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

import smoid.languages
import paste
import paste.lang
import paste.model
import paste.util
import paste.web

class Pasty(paste.web.RequestHandler):

    def __init__(self):
        paste.web.RequestHandler.__init__(self)
        self.set_module("page.pasties.pasty.__init__")
        self.use_style(paste.url("style/code.css"))
        self.highlights = set([])
        self.has_edited_lines = False
        self.has_highlights = False
        self.edited_lines = {}
        self.lines = []
        self.line_count = 0
        self.parent = None

    def update_highlights(self, hl_string):
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
        pasties = paste.model.Pasty.all()
        pasties.filter("slug =", pasty_slug)
        self.pasty = pasties.get()
        self.pasty_slug = pasty_slug
        self.get_parent_paste()

        if self.pasty == None:
            self.get_404()
        else:
            self.get_200()

    def get_200(self):

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


        if self.pasty.language != "":
            lang = paste.lang.get_by_tag(self.pasty.language)
            if lang != None:
                self.content["language"] = lang.name
                self.content["u_language"] = lang.url

        tc = paste.tag.TagCollection()
        tc.import_string(self.pasty.tags)
        thread_pastes = self.get_thread_pastes()

        self.content["is_thread"] = len(thread_pastes) > 1
        self.content["u_thread"] = paste.url("threads/%s.atom", self.pasty.thread)
        if self.content["is_thread"] == True:
            self.content["thread_pastes"] = thread_pastes
        self.content["h1"] = "p" + self.pasty_slug
        self.content["page-title"] =  cgi.escape(self.pasty.title)
        self.content["pasty_title"] =  cgi.escape(self.pasty.title)
        self.content["pasty_slug"] = self.pasty.slug
        self.content["pasty_is_moderated"] = self.pasty.is_moderated
        if self.pasty.characters:
            self.content["pasty_size"] = paste.util.make_filesize_readable(self.pasty.characters)
        self.content["pasty_loc"] = self.pasty.lines
        self.content["pasty_lines"] = lines
        self.content["pasty_code"] = code
        self.content["pasty_tags"] = ", ".join(tc.tags)
        self.content["user_name"] = self.pasty.posted_by_user_name
        self.content["u_user"] = paste.url("users/%s", self.pasty.posted_by_user_name)
        if self.pasty.user:
            self.content["u_gravatar"] = self.pasty.user.get_gravatar(16)

        self.content["posted_at"] = self.pasty.posted_at.strftime("%b, %d %Y at %H:%M")
        if self.pasty.language:
            lang = smoid.languages.languages[self.pasty.language]
            self.content["pasty_language_name"] = lang["name"]
            self.content["pasty_language_url"] = lang["home_url"]
        self.content["u"] = paste.url("%s", self.pasty_slug)
        self.content["u_fork"] = paste.url("%s/fork", self.pasty_slug)
        self.content["u_raw_text"] = paste.url("%s.txt", self.pasty_slug)
        self.content["u_atom"] = paste.url("%s.atom", self.pasty_slug)

        self.add_atom_feed(paste.url("%s.atom", self.pasty_slug), self.pasty_slug + " (Atom feed)", "alternate")
        self.write_out("page/pasties/pasty/200.html")

        #self.update_expiration_time()

    def get_404(self):
        self.error(404)
        self.content["pasty_slug"] = cgi.escape(self.pasty_slug)
        self.content["u_paste"] = paste.url("")
        self.content["u_pastes"] = paste.url("pastes/")
        self.write_out("page/pasties/pasty/404.html")

    def get_parent_paste(self):
        if self.pasty != None and self.pasty.parent_paste != "":
            qparent = paste.model.Pasty.all()
            qparent.filter("slug =", self.pasty.parent_paste)
            self.parent = qparent.get()
            if self.parent != None:
                self.content["u_parent"] = paste.url("%s", self.parent.slug)
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
        dbqry = paste.model.Pasty.all()
        dbqry.filter("thread =", self.pasty.thread)
        dbqry.order("thread_position")
        dbpastes = dbqry.fetch(1000)

        cur_level = 0
        for dbpaste in dbpastes:
            lpaste = {}
            lpaste["title"] = dbpaste.title
            lpaste["slug"] = dbpaste.slug
            lpaste["user_name"] = dbpaste.posted_by_user_name
            lpaste["is_moderated"] = dbpaste.is_moderated
            lpaste["u"] = paste.url("%s", dbpaste.slug)
            lpaste["u_diff"] = paste.url("%s/diff/%s", self.pasty.slug, dbpaste.slug)
            lpaste["ident"] = ("&nbsp;&nbsp;&nbsp;&nbsp;" * dbpaste.thread_level)

            if dbpaste.language:
                lpaste["language_name"] = smoid.languages.languages[dbpaste.language]["name"]
                lpaste["u_language_image"] = smoid.languages.languages[dbpaste.language]["u_icon"]
            else:
                lpaste["u_language_image"] = paste.url("images/silk/page_white_text.png")

            if dbpaste.characters > default_chars:
                lpaste["diff_size"] = paste.util.make_filesize_readable(dbpaste.characters - default_chars)
                lpaste["diff_size"].append("+")
            else:
                lpaste["diff_size"] = paste.util.make_filesize_readable(default_chars - dbpaste.characters)
                lpaste["diff_size"].append("-")

            if dbpaste.lines > default_loc:
                lpaste["diff_loc"] = "+"
            else:
                lpaste["diff_loc"] = ""
            lpaste["diff_loc"] += str(dbpaste.lines - default_loc)

            if dbpaste.thread_level > cur_level:
                cur_level = dbpaste.thread_level
                lpaste["open_list"] = 1
            elif dbpaste.thread_level < cur_level:
                cur_level = dbpaste.thread_level
                lpaste["close_list"] = 1
            pastes.append(lpaste)
        return pastes

    def update_expiration_time(self):
        if self.pasty != None:
            self.pasty.expired_at = datetime.datetime.now() + paste.config["pasty_expiration_delta"]
            self.put()

