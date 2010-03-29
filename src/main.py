#!/usr/bin/env python
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


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import page.error.error404
import page.languages.autodetected
import page.pasties.add
import page.pasties.index
import page.pasties.pasty
import page.pasties.pasty_txt
import page.pasties.pasty_atom
import page.pasties.sitemap
import page.threads.thread_atom

pages = [
    ('/', page.pasties.add.Add),
    ('/(P[a-zA-Z0-9_-]+)', page.pasties.pasty.Pasty),
    ('/(P[a-zA-Z0-9_-]+)/fork', page.pasties.add.Add),
    ('/(P[a-zA-Z0-9_-]+).txt', page.pasties.pasty_txt.PastyTxt),
    ('/(P[a-zA-Z0-9_-]+).atom', page.pasties.pasty_atom.PastyAtom),
    ('/pastes/', page.pasties.index.Index),
    ('/threads/(P[a-zA-Z0-9_-]+).atom', page.threads.thread_atom.ThreadAtom),
    ('/sitemap.xml', page.pasties.sitemap.Sitemap),
    ('/languages/auto-detected', page.languages.autodetected.AutoDetected),
    ('/.*', page.error.error404.Error404)
]
application = webapp.WSGIApplication(pages, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


