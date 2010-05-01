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

import smoid.languages
import app.model
import app.web

class Features (app.web.RequestHandler):

    def get(self):
        self.set_module(__name__ + ".__init__")

        self.path.add("About", app.url("about"))
        self.path.add("Features", app.url("about/features"))

        self.write_out("page/about/features/200.html")
