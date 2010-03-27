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

import math

class Paging:

    def __init__(self):
        self.items = 0
        self.page = 0
        self.pages = []
        self.page_count = 0
        self.page_length = 0
        self.page_url = ""
        self.prepared = False

    def make_page(self, i):
        if i == - 1:
            return (-1, "", self.page == i)
        else:
            return (i, self.page_url.replace("{page}", str(i)), self.page == i)

    def prepare(self):
        self.prepared = True

    def append_page_range(self, start, end):
        for i in range(int(start), int(end)):
            self.pages.append(self.make_page(i))

class CursorPaging (Paging):

    def __init__(self):
        Paging.__init__(self)
        self.cursor_margin = 0
        self.left_margin = 0
        self.right_margin = 0

    def prepare(self):
        self.page_count = (math.ceil(float(self.items) / float(self.page_length)))

        if (self.left_margin + self.cursor_margin + 1) < self.page:
            self.append_page_range(1, self.left_margin + 1)
            self.pages.append(self.make_page(-1))
        else:
            self.append_page_range(1, min(self.page - self.cursor_margin, self.left_margin + 1))

        self.append_page_range(max(1, self.page - self.cursor_margin), min(self.page + self.cursor_margin + 1, self.page_count + 1))

        if (self.page_count - self.right_margin - self.cursor_margin) > self.page:
            self.pages.append(self.make_page(-1))
            self.append_page_range(self.page_count - self.right_margin + 1, self.page_count + 1)
        else:
            self.append_page_range(max(self.page + 1, self.page + self.cursor_margin + 1), self.page_count + 1)
            pass

        self.prepared = True
